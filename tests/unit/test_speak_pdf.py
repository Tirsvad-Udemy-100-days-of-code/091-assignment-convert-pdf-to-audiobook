from collections.abc import Callable
from pathlib import Path

import pytest
from tests.fakes import FakePlayer, FakeSpeechEngine

from pdf_to_audiobook.application import speak_pdf
from pdf_to_audiobook.domain.errors import EmptyTextError, PdfTextError
from pdf_to_audiobook.infrastructure.pdf_reader import extract_text_from_pdf


def test_speak_pdf_speaks_pages_in_order(
    make_pdf: Callable[[list[str]], Path],
) -> None:
    pdf = make_pdf(["Page one text.", "Page two text.", "Page three text."])
    engine, player = FakeSpeechEngine(), FakePlayer()
    count = speak_pdf(pdf, engine, player, extract_text_from_pdf)
    assert engine.texts == ["Page one text.", "Page two text.", "Page three text."]
    assert count == 3
    assert len(player.clips) == 3


def test_speak_pdf_reports_progress(make_pdf: Callable[[list[str]], Path]) -> None:
    pdf = make_pdf(["One.", "Two."])
    calls: list[tuple[int, int]] = []
    speak_pdf(
        pdf,
        FakeSpeechEngine(),
        FakePlayer(),
        extract_text_from_pdf,
        lambda done, total: calls.append((done, total)),
    )
    assert calls == [(1, 2), (2, 2)]


def test_speak_pdf_stops_between_chunks(
    make_pdf: Callable[[list[str]], Path],
) -> None:
    pdf = make_pdf(["One.", "Two.", "Three."])
    engine, player = FakeSpeechEngine(), FakePlayer()
    count = speak_pdf(
        pdf,
        engine,
        player,
        extract_text_from_pdf,
        should_stop=lambda: len(player.clips) >= 1,
    )
    assert count == 1
    assert engine.texts == ["One."]


def test_speak_pdf_rejects_blank_text() -> None:
    with pytest.raises(EmptyTextError):
        speak_pdf("x.pdf", FakeSpeechEngine(), FakePlayer(), lambda _path: "  \n ")


def test_speak_pdf_rejects_pdf_without_text(
    make_pdf: Callable[[list[str]], Path],
) -> None:
    with pytest.raises(PdfTextError):
        speak_pdf(
            make_pdf([""]), FakeSpeechEngine(), FakePlayer(), extract_text_from_pdf
        )


def test_speak_pdf_missing_file_raises_pdf_text_error(tmp_path: Path) -> None:
    with pytest.raises(PdfTextError, match="not found"):
        speak_pdf(
            tmp_path / "missing.pdf",
            FakeSpeechEngine(),
            FakePlayer(),
            extract_text_from_pdf,
        )
