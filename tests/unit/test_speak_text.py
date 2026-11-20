import pytest
from tests.fakes import FakePlayer, FakeSpeechEngine

from pdf_to_audiobook.application import speak_text
from pdf_to_audiobook.domain.errors import (
    EmptyTextError,
    PlaybackError,
    SpeechEngineError,
)

TEXT = "First paragraph here.\n\nSecond paragraph here."


def test_speak_text_plays_each_chunk_in_order() -> None:
    engine, player = FakeSpeechEngine(), FakePlayer()
    count = speak_text(TEXT, engine, player)
    assert engine.texts == ["First paragraph here.", "Second paragraph here."]
    assert count == 2
    assert len(player.clips) == 2


def test_speak_text_reports_progress_after_each_chunk() -> None:
    calls: list[tuple[int, int]] = []
    speak_text(
        TEXT, FakeSpeechEngine(), FakePlayer(), lambda d, t: calls.append((d, t))
    )
    assert calls == [(1, 2), (2, 2)]


@pytest.mark.parametrize("text", ["", "   \n\t "])
def test_speak_text_rejects_blank_text(text: str) -> None:
    player = FakePlayer()
    with pytest.raises(EmptyTextError):
        speak_text(text, FakeSpeechEngine(), player)
    assert player.clips == []


def test_speak_text_propagates_engine_error() -> None:
    engine = FakeSpeechEngine(error=SpeechEngineError("boom"))
    player = FakePlayer()
    with pytest.raises(SpeechEngineError):
        speak_text(TEXT, engine, player)
    assert player.clips == []


def test_speak_text_propagates_playback_error() -> None:
    with pytest.raises(PlaybackError):
        speak_text(TEXT, FakeSpeechEngine(), FakePlayer(error=PlaybackError("no")))


def test_speak_text_stops_between_chunks() -> None:
    engine, player = FakeSpeechEngine(), FakePlayer()
    count = speak_text(TEXT, engine, player, should_stop=lambda: bool(player.clips))
    assert count == 1
    assert engine.texts == ["First paragraph here."]
