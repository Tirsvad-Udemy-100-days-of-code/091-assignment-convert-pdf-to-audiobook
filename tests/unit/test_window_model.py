from tests.fakes import FakePlayer, FakeSpeechEngine

from pdf_to_audiobook.constants import STATUS_DONE, STATUS_READY
from pdf_to_audiobook.domain.errors import PlaybackError, SpeechEngineError
from pdf_to_audiobook.presentation.window_model import SpeakViewModel


def test_new_model_is_ready_and_idle() -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer())
    assert (model.status, model.busy) == (STATUS_READY, False)


def test_can_speak_is_false_for_blank_text() -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer())
    assert not model.can_speak("  \n")
    assert model.can_speak("Hello.")


def test_speak_plays_text_and_ends_done() -> None:
    player = FakePlayer()
    model = SpeakViewModel(FakeSpeechEngine(), player)
    model.speak("Hello there.")
    assert model.status == STATUS_DONE
    assert not model.busy
    assert len(player.clips) == 1


def test_speak_is_disabled_while_busy() -> None:
    seen: list[tuple[str, bool, bool]] = []

    class Spy:
        def play(self, clip: object) -> None:
            seen.append((model.status, model.busy, model.can_speak("Hello.")))

    model = SpeakViewModel(FakeSpeechEngine(), Spy())  # type: ignore[arg-type]
    model.speak("Hello.")
    assert seen == [("Speaking...", True, False)]
    assert model.can_speak("Hello.")


def test_speak_shows_engine_error_as_message_and_clears_busy() -> None:
    engine = FakeSpeechEngine(error=SpeechEngineError("model broke"))
    model = SpeakViewModel(engine, FakePlayer())
    model.speak("Hello.")
    assert model.status == "error: model broke"
    assert not model.busy


def test_speak_shows_playback_error_as_message() -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(error=PlaybackError("no")))
    model.speak("Hello.")
    assert model.status == "error: no"
    assert not model.busy


def test_speak_shows_empty_text_error_as_message() -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer())
    model.speak("   ")
    assert model.status == "error: There is no text to speak."
    assert not model.busy


def test_on_change_is_called_for_each_update() -> None:
    changes: list[str] = []
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer())
    model.on_change = lambda: changes.append(model.status)
    model.speak("Hello.")
    assert changes == ["Speaking...", "Done"]
