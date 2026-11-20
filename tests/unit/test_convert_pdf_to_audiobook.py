import io
import wave
from collections.abc import Callable
from pathlib import Path

import pytest
from tests.fakes import FakeSpeechEngine

from pdf_to_audiobook.application.convert_pdf_to_audiobook import (
    convert_pdf_to_audiobook,
)
from pdf_to_audiobook.constants import MAX_CHUNK_CHARS
from pdf_to_audiobook.domain.errors import (
    AudiobookError,
    OutputWriteError,
    PdfTextError,
    SpeechEngineError,
)

PARAGRAPH = "First paragraph here.\n\nSecond paragraph here.\n\nThird one."


def extractor(text: str) -> Callable[[Path], str]:
    def _extract(path: Path) -> str:
        return text

    return _extract


def run(
    tmp_path: Path,
    text: str = PARAGRAPH,
    engine: FakeSpeechEngine | None = None,
    name: str = "out.wav",
    progress: Callable[[int, int], None] | None = None,
) -> Path:
    return convert_pdf_to_audiobook(
        tmp_path / "book.pdf",
        tmp_path / name,
        engine or FakeSpeechEngine(),
        extractor(text),
        progress,
    )


def test_engine_receives_chunks_in_order(tmp_path: Path) -> None:
    engine = FakeSpeechEngine()
    run(tmp_path, engine=engine)
    assert engine.texts == [
        "First paragraph here.",
        "Second paragraph here.",
        "Third one.",
    ]


def test_extractor_receives_pdf_path(tmp_path: Path) -> None:
    seen: list[Path] = []

    def _extract(path: Path) -> str:
        seen.append(path)
        return "Hello."

    convert_pdf_to_audiobook(
        str(tmp_path / "b.pdf"), tmp_path / "o.wav", FakeSpeechEngine(), _extract
    )
    assert seen == [tmp_path / "b.pdf"]


def test_progress_is_called_after_each_chunk(tmp_path: Path) -> None:
    calls: list[tuple[int, int]] = []
    run(tmp_path, progress=lambda done, total: calls.append((done, total)))
    assert calls == [(1, 3), (2, 3), (3, 3)]


def test_output_is_valid_wav_with_all_chunks(tmp_path: Path) -> None:
    result = run(tmp_path)
    with wave.open(io.BytesIO(result.read_bytes()), "rb") as reader:
        assert reader.getnframes() == 3 * int(22050 * 0.1)


def test_output_is_returned_as_path(tmp_path: Path) -> None:
    assert run(tmp_path) == tmp_path / "out.wav"


def test_string_output_path_is_returned_as_path(tmp_path: Path) -> None:
    result = convert_pdf_to_audiobook(
        "b.pdf", str(tmp_path / "o.wav"), FakeSpeechEngine(), lambda p: "Hi."
    )
    assert isinstance(result, Path)


def test_parent_folder_is_created(tmp_path: Path) -> None:
    result = run(tmp_path, name="deep/er/out.wav")
    assert result.is_file()


def test_wrong_suffix_raises_and_writes_nothing(tmp_path: Path) -> None:
    with pytest.raises(AudiobookError, match=".wav"):
        run(tmp_path, name="out.mp3")
    assert not (tmp_path / "out.mp3").exists()


def test_no_chunks_raises(tmp_path: Path) -> None:
    with pytest.raises(AudiobookError, match="no text"):
        run(tmp_path, text="   \n\n  ")


def test_extractor_error_is_propagated(tmp_path: Path) -> None:
    def _fail(path: Path) -> str:
        raise PdfTextError("boom")

    with pytest.raises(PdfTextError, match="boom"):
        convert_pdf_to_audiobook(
            tmp_path / "b.pdf", tmp_path / "o.wav", FakeSpeechEngine(), _fail
        )


def test_engine_error_is_propagated(tmp_path: Path) -> None:
    with pytest.raises(SpeechEngineError, match="bad"):
        run(tmp_path, engine=FakeSpeechEngine(error=SpeechEngineError("bad")))


def test_unwritable_output_raises_audiobook_error(tmp_path: Path) -> None:
    blocker = tmp_path / "file"
    blocker.write_text("x")
    with pytest.raises(OutputWriteError, match="Cannot write"):
        run(tmp_path, name="file/out.wav")


def test_long_text_is_split_by_chunk_limit(tmp_path: Path) -> None:
    engine = FakeSpeechEngine()
    run(tmp_path, text="word " * MAX_CHUNK_CHARS, engine=engine)
    assert len(engine.texts) > 1
    assert all(len(text) <= MAX_CHUNK_CHARS for text in engine.texts)
