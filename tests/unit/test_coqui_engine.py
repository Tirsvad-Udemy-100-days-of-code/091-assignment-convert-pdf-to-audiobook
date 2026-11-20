import subprocess
import sys
import types
from pathlib import Path

import pytest
from tests.fakes import build_wav_bytes

from pdf_to_audiobook.constants import DEFAULT_MODEL_NAME, MAX_CHUNK_CHARS
from pdf_to_audiobook.domain.errors import EngineUnavailableError, SpeechEngineError
from pdf_to_audiobook.infrastructure.coqui_engine import (
    CoquiSpeechEngine,
    TtsModel,
    load_coqui_model,
)


class StubModel:
    def __init__(
        self,
        wav: bytes | None = None,
        error: Exception | None = None,
    ) -> None:
        self._wav = build_wav_bytes(sample_rate=16000) if wav is None else wav
        self._error = error
        self.texts: list[str] = []

    def tts_to_file(self, *, text: str, file_path: str) -> object:
        self.texts.append(text)
        if self._error is not None:
            raise self._error
        Path(file_path).write_bytes(self._wav)
        return None


class CountingLoader:
    def __init__(self, model: TtsModel) -> None:
        self.model = model
        self.names: list[str] = []

    def __call__(self, model_name: str) -> TtsModel:
        self.names.append(model_name)
        return self.model


def test_synthesize_returns_clip_with_wav_parameters() -> None:
    engine = CoquiSpeechEngine(loader=CountingLoader(StubModel()))
    clip = engine.synthesize("Hello there.")
    assert clip.sample_rate == 16000
    assert clip.channels == 1
    assert clip.sample_width == 2
    assert clip.data == build_wav_bytes(sample_rate=16000)


def test_model_loads_once_for_two_calls() -> None:
    model = StubModel()
    loader = CountingLoader(model)
    engine = CoquiSpeechEngine(model_name="my-model", loader=loader)
    assert loader.names == []
    engine.synthesize("One.")
    engine.synthesize("Two.")
    assert loader.names == ["my-model"]
    assert model.texts == ["One.", "Two."]


def test_default_model_name_is_used() -> None:
    loader = CountingLoader(StubModel())
    CoquiSpeechEngine(loader=loader).synthesize("Hi.")
    assert loader.names == [DEFAULT_MODEL_NAME]


def test_importing_module_does_not_import_tts() -> None:
    code = (
        "import sys; import pdf_to_audiobook.infrastructure.coqui_engine; "
        "sys.exit(1 if 'TTS' in sys.modules else 0)"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("text", ["", "   ", "\n\t"])
def test_blank_text_is_rejected(text: str) -> None:
    engine = CoquiSpeechEngine(loader=CountingLoader(StubModel()))
    with pytest.raises(SpeechEngineError):
        engine.synthesize(text)


def test_text_at_the_limit_is_accepted() -> None:
    engine = CoquiSpeechEngine(loader=CountingLoader(StubModel()))
    assert engine.synthesize("a" * MAX_CHUNK_CHARS).data


def test_text_over_the_limit_is_rejected() -> None:
    engine = CoquiSpeechEngine(loader=CountingLoader(StubModel()))
    with pytest.raises(SpeechEngineError, match="limit"):
        engine.synthesize("a" * (MAX_CHUNK_CHARS + 1))


def test_loader_failure_propagates_as_unavailable() -> None:
    def failing_loader(model_name: str) -> TtsModel:
        raise EngineUnavailableError("no model")

    engine = CoquiSpeechEngine(loader=failing_loader)
    with pytest.raises(EngineUnavailableError):
        engine.synthesize("Hello.")


def test_synthesis_failure_is_wrapped() -> None:
    cause = RuntimeError("bad")
    engine = CoquiSpeechEngine(loader=CountingLoader(StubModel(error=cause)))
    with pytest.raises(SpeechEngineError) as info:
        engine.synthesize("Hello.")
    assert info.value.__cause__ is cause


def test_empty_output_file_is_rejected() -> None:
    engine = CoquiSpeechEngine(loader=CountingLoader(StubModel(wav=b"")))
    with pytest.raises(SpeechEngineError, match="empty"):
        engine.synthesize("Hello.")


def test_missing_output_file_is_rejected() -> None:
    class SilentModel:
        def tts_to_file(self, *, text: str, file_path: str) -> object:
            return None

    engine = CoquiSpeechEngine(loader=CountingLoader(SilentModel()))
    with pytest.raises(SpeechEngineError, match="no audio file"):
        engine.synthesize("Hello.")


def test_invalid_wav_is_rejected() -> None:
    engine = CoquiSpeechEngine(loader=CountingLoader(StubModel(wav=b"not a wav")))
    with pytest.raises(SpeechEngineError, match="invalid WAV"):
        engine.synthesize("Hello.")


def test_default_loader_creates_model_from_tts_api(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created: list[str] = []

    class FakeTts:
        def __init__(self, model_name: str) -> None:
            created.append(model_name)

    package = types.ModuleType("TTS")
    api = types.ModuleType("TTS.api")
    api.TTS = FakeTts  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "TTS", package)
    monkeypatch.setitem(sys.modules, "TTS.api", api)
    model = load_coqui_model("some-model")
    assert isinstance(model, FakeTts)
    assert created == ["some-model"]


def test_default_loader_reports_missing_install(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "TTS.api", None)
    with pytest.raises(EngineUnavailableError, match="pip install -e"):
        load_coqui_model("some-model")


def test_default_loader_wraps_model_load_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class BrokenTts:
        def __init__(self, model_name: str) -> None:
            raise OSError("download failed")

    api = types.ModuleType("TTS.api")
    api.TTS = BrokenTts  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "TTS", types.ModuleType("TTS"))
    monkeypatch.setitem(sys.modules, "TTS.api", api)
    with pytest.raises(EngineUnavailableError, match="download failed"):
        load_coqui_model("some-model")


def test_on_loading_is_called_once_for_two_calls() -> None:
    calls: list[str] = []
    engine = CoquiSpeechEngine(
        loader=CountingLoader(StubModel()), on_loading=lambda: calls.append("load")
    )
    engine.synthesize("One.")
    engine.synthesize("Two.")
    assert calls == ["load"]


def test_on_loading_is_called_before_the_model_loads() -> None:
    order: list[str] = []

    def loader(model_name: str) -> TtsModel:
        order.append("loader")
        return StubModel()

    engine = CoquiSpeechEngine(loader=loader, on_loading=lambda: order.append("notice"))
    engine.synthesize("One.")
    assert order == ["notice", "loader"]


def test_no_callback_means_no_error() -> None:
    CoquiSpeechEngine(loader=CountingLoader(StubModel())).synthesize("One.")
