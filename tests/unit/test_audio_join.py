import io
import wave

import pytest
from tests.fakes import build_wav_bytes

from pdf_to_audiobook.domain.audio_join import join_wav_clips
from pdf_to_audiobook.domain.errors import AudiobookError, AudioJoinError
from pdf_to_audiobook.domain.speech import AudioClip


def make_clip(
    sample_rate: int = 22050,
    channels: int = 1,
    sample_width: int = 2,
    seconds: float = 0.1,
) -> AudioClip:
    return AudioClip(
        data=build_wav_bytes(sample_rate, channels, sample_width, seconds),
        sample_rate=sample_rate,
        channels=channels,
        sample_width=sample_width,
    )


def read_params(clip: AudioClip) -> tuple[int, int, int, int]:
    with wave.open(io.BytesIO(clip.data), "rb") as reader:
        return (
            reader.getframerate(),
            reader.getnchannels(),
            reader.getsampwidth(),
            reader.getnframes(),
        )


def test_join_adds_frames_and_keeps_parameters() -> None:
    first, second = make_clip(seconds=0.1), make_clip(seconds=0.2)
    joined = join_wav_clips([first, second])
    frames = read_params(first)[3] + read_params(second)[3]
    assert read_params(joined) == (22050, 1, 2, frames)
    assert (joined.sample_rate, joined.channels, joined.sample_width) == (22050, 1, 2)


def test_join_single_clip_returns_equal_clip() -> None:
    clip = make_clip()
    assert join_wav_clips([clip]) == clip


def test_join_empty_sequence_raises() -> None:
    with pytest.raises(AudioJoinError, match="no audio clips"):
        join_wav_clips([])


def test_audio_join_error_is_audiobook_error() -> None:
    assert issubclass(AudioJoinError, AudiobookError)


@pytest.mark.parametrize(
    ("other", "name"),
    [
        (make_clip(sample_rate=16000), "sample_rate"),
        (make_clip(channels=2), "channels"),
        (make_clip(sample_width=1), "sample_width"),
    ],
)
def test_join_mismatched_parameter_raises(other: AudioClip, name: str) -> None:
    with pytest.raises(AudioJoinError, match=name):
        join_wav_clips([make_clip(), other])


def test_join_corrupt_bytes_raises() -> None:
    corrupt = AudioClip(
        data=b"not a wav", sample_rate=22050, channels=1, sample_width=2
    )
    with pytest.raises(AudioJoinError, match="not a valid WAV"):
        join_wav_clips([make_clip(), corrupt])
