from pathlib import Path

import pytest
from tests.fakes import FakePlayer, FakeSpeechEngine, fake_extract_text

from pdf_to_audiobook.constants import STATUS_DONE, STATUS_READY
from pdf_to_audiobook.domain.errors import (
    PdfTextError,
    PlaybackError,
    SpeechEngineError,
)
from pdf_to_audiobook.presentation.window_model import SpeakViewModel


def test_new_model_is_ready_and_idle() -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(), fake_extract_text())
    assert (model.status, model.busy) == (STATUS_READY, False)


def test_can_speak_is_false_for_blank_text() -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(), fake_extract_text())
    assert not model.can_speak("  \n")
    assert model.can_speak("Hello.")


def test_speak_plays_text_and_ends_done() -> None:
    player = FakePlayer()
    model = SpeakViewModel(FakeSpeechEngine(), player, fake_extract_text())
    model.speak("Hello there.")
    assert model.status == STATUS_DONE
    assert not model.busy
    assert len(player.clips) == 1


def test_speak_is_disabled_while_busy() -> None:
    seen: list[tuple[str, bool, bool]] = []

    class Spy:
        def play(self, clip: object) -> None:
            seen.append((model.status, model.busy, model.can_speak("Hello.")))

    model = SpeakViewModel(FakeSpeechEngine(), Spy(), fake_extract_text())  # type: ignore[arg-type]
    model.speak("Hello.")
    assert seen == [("Speaking...", True, False)]
    assert model.can_speak("Hello.")


def test_speak_shows_engine_error_as_message_and_clears_busy() -> None:
    engine = FakeSpeechEngine(error=SpeechEngineError("model broke"))
    model = SpeakViewModel(engine, FakePlayer(), fake_extract_text())
    model.speak("Hello.")
    assert model.status == "error: model broke"
    assert not model.busy


def test_speak_shows_playback_error_as_message() -> None:
    model = SpeakViewModel(
        FakeSpeechEngine(), FakePlayer(error=PlaybackError("no")), fake_extract_text()
    )
    model.speak("Hello.")
    assert model.status == "error: no"
    assert not model.busy


def test_speak_shows_empty_text_error_as_message() -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(), fake_extract_text())
    model.speak("   ")
    assert model.status == "error: There is no text to speak."
    assert not model.busy


def test_on_change_is_called_for_each_update() -> None:
    changes: list[str] = []
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(), fake_extract_text())
    model.on_change = lambda: changes.append(model.status)
    model.speak("Hello.")
    assert changes == ["Speaking...", "Done"]


def test_open_pdf_shows_file_name_then_done() -> None:
    seen: list[str] = []
    player = FakePlayer()
    model = SpeakViewModel(FakeSpeechEngine(), player, fake_extract_text())
    model.on_change = lambda: seen.append(model.status)
    model.open_pdf(Path("some") / "book.pdf")
    assert seen == ["Speaking: book.pdf", "Done"]
    assert len(player.clips) == 2
    assert not model.busy


def test_open_pdf_shows_extract_error_as_message() -> None:
    def extract(path: Path) -> str:
        raise PdfTextError("PDF file not found: x.pdf")

    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(), extract)
    model.open_pdf("x.pdf")
    assert model.status == "error: PDF file not found: x.pdf"
    assert not model.busy


def test_open_pdf_shows_empty_pdf_as_message() -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(), fake_extract_text("  "))
    model.open_pdf("blank.pdf")
    assert model.status.startswith("error: The PDF has no text")


def test_enabled_states_follow_busy() -> None:
    states: list[tuple[bool, bool, bool]] = []

    class Spy:
        def play(self, clip: object) -> None:
            states.append((model.can_speak("Hi."), model.can_open(), model.can_stop()))

    model = SpeakViewModel(FakeSpeechEngine(), Spy(), fake_extract_text())  # type: ignore[arg-type]
    assert (model.can_speak("Hi."), model.can_open(), model.can_stop()) == (
        True,
        True,
        False,
    )
    model.speak("Hi.")
    assert states == [(False, False, True)]
    assert model.can_open()
    assert not model.can_stop()


def test_stop_ends_speech_between_chunks_and_shows_stopped() -> None:
    engine = FakeSpeechEngine()
    model = SpeakViewModel(engine, FakePlayer(), fake_extract_text())

    class StopAfterFirst:
        def play(self, clip: object) -> None:
            model.stop()

    model = SpeakViewModel(engine, StopAfterFirst(), fake_extract_text())  # type: ignore[arg-type]
    model.speak("First sentence.\n\nSecond sentence.")
    assert engine.texts == ["First sentence."]
    assert model.status == "Stopped"
    assert not model.busy


def test_stop_when_idle_does_nothing_and_next_run_is_not_stopped() -> None:
    player = FakePlayer()
    model = SpeakViewModel(FakeSpeechEngine(), player, fake_extract_text())
    model.stop()
    model.open_pdf("book.pdf")
    assert model.status == "Done"
    assert len(player.clips) == 2


@pytest.mark.parametrize("path", ["book.pdf", Path("book.pdf")])
def test_open_pdf_accepts_str_and_path(path: str | Path) -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(), fake_extract_text())
    model.open_pdf(path)
    assert model.status == "Done"
