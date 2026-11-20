import io
import subprocess
import sys
import wave
from collections.abc import Callable
from pathlib import Path

import pytest
from tests.fakes import FakeSpeechEngine

from pdf_to_audiobook.constants import (
    AUDIO_FILE_SUFFIX,
    DEFAULT_MODEL_NAME,
    EXIT_ERROR,
    EXIT_OK,
    EXIT_USAGE,
)
from pdf_to_audiobook.domain.speech import SpeechEngine
from pdf_to_audiobook.infrastructure import coqui_engine
from pdf_to_audiobook.presentation import cli

MakePdf = Callable[[list[str]], Path]


def assert_valid_wav(path: Path) -> None:
    with wave.open(io.BytesIO(path.read_bytes()), "rb") as reader:
        assert reader.getnframes() > 0


def test_main_converts_pdf_to_wav(
    make_pdf: MakePdf, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    pdf = make_pdf(["Hello world. This is a test."])
    output = tmp_path / "out" / "book.wav"
    engine = FakeSpeechEngine()
    code = cli.main([str(pdf), "-o", str(output)], lambda model: engine)
    captured = capsys.readouterr()
    assert code == EXIT_OK
    assert f"Wrote {output}" in captured.out
    assert "Speaking chunk 1 of 1" in captured.err
    assert engine.texts == ["Hello world. This is a test."]
    assert_valid_wav(output)


def test_main_default_output_replaces_pdf_suffix(make_pdf: MakePdf) -> None:
    pdf = make_pdf(["Some text."])
    code = cli.main([str(pdf)], lambda model: FakeSpeechEngine())
    assert code == EXIT_OK
    assert_valid_wav(pdf.with_suffix(AUDIO_FILE_SUFFIX))


def test_main_missing_pdf_returns_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = cli.main([str(tmp_path / "none.pdf")], lambda model: FakeSpeechEngine())
    assert code == EXIT_ERROR
    assert capsys.readouterr().err.startswith("error: ")


def test_main_engine_error_returns_error(
    make_pdf: MakePdf, capsys: pytest.CaptureFixture[str]
) -> None:
    from pdf_to_audiobook.domain.errors import SpeechEngineError

    pdf = make_pdf(["Some text."])
    engine = FakeSpeechEngine(error=SpeechEngineError("no voice"))
    assert cli.main([str(pdf)], lambda model: engine) == EXIT_ERROR
    assert "error: no voice" in capsys.readouterr().err


def test_main_without_arguments_is_usage_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert cli.main([]) == EXIT_USAGE
    assert "usage" in capsys.readouterr().err.lower()


def test_main_help_returns_ok(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--help"]) == EXIT_OK
    assert "usage" in capsys.readouterr().out.lower()


def test_main_model_reaches_factory(make_pdf: MakePdf) -> None:
    models: list[str] = []

    def factory(model: str) -> SpeechEngine:
        models.append(model)
        return FakeSpeechEngine()

    pdf = make_pdf(["Some text."])
    cli.main([str(pdf), "--model", "my/model"], factory)
    cli.main([str(pdf)], factory)
    assert models == ["my/model", DEFAULT_MODEL_NAME]


def test_main_default_factory_builds_coqui_engine(
    make_pdf: MakePdf, monkeypatch: pytest.MonkeyPatch
) -> None:
    built: list[str] = []

    class StubEngine(FakeSpeechEngine):
        def __init__(self, model_name: str) -> None:
            super().__init__()
            built.append(model_name)

    monkeypatch.setattr(cli, "CoquiSpeechEngine", StubEngine)
    assert cli.main([str(make_pdf(["Some text."]))]) == EXIT_OK
    assert built == [DEFAULT_MODEL_NAME]
    assert coqui_engine.CoquiSpeechEngine is not StubEngine


def test_module_help_runs_in_subprocess() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pdf_to_audiobook", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()
