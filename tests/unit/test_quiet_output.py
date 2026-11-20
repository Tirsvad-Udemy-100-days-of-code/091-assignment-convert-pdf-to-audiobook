import logging
import os
import sys
from pathlib import Path

import pytest
from tests.fakes import build_wav_bytes

from pdf_to_audiobook.constants import QUIET_ENVIRONMENT, QUIET_LOGGER_NAMES
from pdf_to_audiobook.domain.errors import SpeechEngineError
from pdf_to_audiobook.infrastructure.coqui_engine import CoquiSpeechEngine, TtsModel
from pdf_to_audiobook.infrastructure.quiet_output import quiet_output

STDOUT_TEXT = "phoneme text on stdout"
STDERR_TEXT = "progress bar on stderr"
LOG_TEXT = "warning from the library logger"


class NoisyModel:
    """A model that talks on stdout, stderr and a library logger."""

    def __init__(self, error: Exception | None = None) -> None:
        self._error = error

    def tts_to_file(self, *, text: str, file_path: str) -> object:
        print(STDOUT_TEXT)
        print(STDERR_TEXT, file=sys.stderr)
        logging.getLogger("TTS").warning(LOG_TEXT)
        if self._error is not None:
            raise self._error
        Path(file_path).write_bytes(build_wav_bytes())
        return None


def noisy_loader(model_name: str) -> TtsModel:
    print(STDOUT_TEXT)
    return NoisyModel()


def test_output_is_hidden_by_default(
    capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.DEBUG)
    CoquiSpeechEngine(loader=noisy_loader).synthesize("Hello there.")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert LOG_TEXT not in caplog.text


def test_output_is_shown_with_verbose(
    capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.DEBUG)
    CoquiSpeechEngine(loader=noisy_loader, verbose=True).synthesize("Hello there.")
    captured = capsys.readouterr()
    assert STDOUT_TEXT in captured.out
    assert STDERR_TEXT in captured.err
    assert LOG_TEXT in caplog.text


def test_error_of_the_model_propagates_and_state_is_restored() -> None:
    cause = ValueError("model broke")
    engine = CoquiSpeechEngine(loader=lambda _name: NoisyModel(error=cause))
    stdout, stderr = sys.stdout, sys.stderr
    levels = {name: logging.getLogger(name).level for name in QUIET_LOGGER_NAMES}
    with pytest.raises(SpeechEngineError, match="model broke"):
        engine.synthesize("Hello there.")
    assert (sys.stdout, sys.stderr) == (stdout, stderr)
    assert levels == {n: logging.getLogger(n).level for n in QUIET_LOGGER_NAMES}


def test_quiet_output_restores_everything_after_an_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TQDM_DISABLE", "0")
    monkeypatch.delenv("HF_HUB_DISABLE_PROGRESS_BARS", raising=False)
    logging.getLogger("torch").setLevel(logging.INFO)
    stdout, stderr = sys.stdout, sys.stderr
    with pytest.raises(RuntimeError, match="real error"), quiet_output(True):
        assert os.environ["TQDM_DISABLE"] == QUIET_ENVIRONMENT["TQDM_DISABLE"]
        assert sys.stdout is not stdout
        raise RuntimeError("real error")
    assert (sys.stdout, sys.stderr) == (stdout, stderr)
    assert logging.getLogger("torch").level == logging.INFO
    assert os.environ["TQDM_DISABLE"] == "0"
    assert "HF_HUB_DISABLE_PROGRESS_BARS" not in os.environ
    logging.getLogger("torch").setLevel(logging.NOTSET)


def test_quiet_output_disabled_changes_nothing(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with quiet_output(False):
        print(STDOUT_TEXT)
    assert STDOUT_TEXT in capsys.readouterr().out


def test_model_load_errors_are_not_swallowed() -> None:
    def failing_loader(model_name: str) -> TtsModel:
        raise SpeechEngineError("cannot load")

    with pytest.raises(SpeechEngineError, match="cannot load"):
        CoquiSpeechEngine(loader=failing_loader).synthesize("Hi.")
