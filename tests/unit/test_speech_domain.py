import dataclasses

import pytest
from tests.fakes import FakeSpeechEngine

from pdf_to_audiobook.domain.errors import (
    AudiobookError,
    EngineUnavailableError,
    SpeechEngineError,
)
from pdf_to_audiobook.domain.speech import AudioClip, SpeechEngine


def test_audio_clip_is_frozen() -> None:
    clip = AudioClip(data=b"RIFF", sample_rate=22050, channels=1, sample_width=2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        clip.sample_rate = 8000  # type: ignore[misc]


def test_audio_clip_holds_its_parameters() -> None:
    clip = AudioClip(data=b"abc", sample_rate=22050, channels=1, sample_width=2)
    assert (clip.data, clip.sample_rate, clip.channels, clip.sample_width) == (
        b"abc",
        22050,
        1,
        2,
    )


def test_fake_engine_satisfies_the_port() -> None:
    engine: SpeechEngine = FakeSpeechEngine()
    clip = engine.synthesize("Hello.")
    assert clip.data.startswith(b"RIFF")


def test_fake_engine_records_texts() -> None:
    engine = FakeSpeechEngine()
    engine.synthesize("One.")
    engine.synthesize("Two.")
    assert engine.texts == ["One.", "Two."]


def test_fake_engine_raises_given_error() -> None:
    engine = FakeSpeechEngine(error=SpeechEngineError("boom"))
    with pytest.raises(SpeechEngineError, match="boom"):
        engine.synthesize("One.")


def test_error_hierarchy() -> None:
    assert issubclass(SpeechEngineError, AudiobookError)
    assert issubclass(EngineUnavailableError, SpeechEngineError)
