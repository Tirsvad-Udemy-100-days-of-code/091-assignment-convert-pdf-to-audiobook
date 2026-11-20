"""@brief Join WAV clips into one WAV clip with the standard library."""

import io
import wave
from collections.abc import Sequence

from pdf_to_audiobook.constants import WAV_READ_MODE, WAV_WRITE_MODE
from pdf_to_audiobook.domain.errors import AudioJoinError
from pdf_to_audiobook.domain.speech import AudioClip


def join_wav_clips(clips: Sequence[AudioClip]) -> AudioClip:
    """!@brief Join WAV clips, in order, into one WAV clip.

    @param clips The clips to join; all must have the same audio parameters.
    @return One clip with the frames of every clip; a single clip is returned as is.
    @throws AudioJoinError If there are no clips, a clip is not a valid WAV file
        or the clips differ in sample rate, channels or sample width.
    """
    if not clips:
        raise AudioJoinError("There are no audio clips to join.")
    first = clips[0]
    if len(clips) == 1:
        return first
    frames = [_read_frames(index, clip) for index, clip in enumerate(clips)]
    for index, clip in enumerate(clips):
        _check_same_parameters(index, first, clip)
    return _write_clip(first, b"".join(frames))


def _read_frames(index: int, clip: AudioClip) -> bytes:
    """!@brief Read the audio frames of a clip.

    @param index Position of the clip, used in the message.
    @param clip The clip to read.
    @return The raw frames.
    @throws AudioJoinError If the bytes are not a valid WAV file.
    """
    try:
        with wave.open(io.BytesIO(clip.data), WAV_READ_MODE) as reader:
            frames: bytes = reader.readframes(reader.getnframes())
            return frames
    except (wave.Error, EOFError) as error:
        raise AudioJoinError(
            f"Audio clip {index + 1} is not a valid WAV file: {error}"
        ) from error


def _check_same_parameters(index: int, first: AudioClip, clip: AudioClip) -> None:
    """!@brief Require a clip to have the audio parameters of the first clip.

    @param index Position of the clip, used in the message.
    @param first The first clip.
    @param clip The clip to compare.
    @return Nothing; the clip is valid when no error is raised.
    @throws AudioJoinError If a parameter differs.
    """
    for name in ("sample_rate", "channels", "sample_width"):
        expected = getattr(first, name)
        actual = getattr(clip, name)
        if actual != expected:
            raise AudioJoinError(
                f"Audio clip {index + 1} has {name} {actual}; expected {expected}."
            )


def _write_clip(template: AudioClip, frames: bytes) -> AudioClip:
    """!@brief Build a WAV clip from frames with the parameters of a template.

    @param template The clip whose parameters are used.
    @param frames The raw frames.
    @return The new clip.
    """
    buffer = io.BytesIO()
    with wave.open(buffer, WAV_WRITE_MODE) as writer:
        writer.setnchannels(template.channels)
        writer.setsampwidth(template.sample_width)
        writer.setframerate(template.sample_rate)
        writer.writeframes(frames)
    return AudioClip(
        data=buffer.getvalue(),
        sample_rate=template.sample_rate,
        channels=template.channels,
        sample_width=template.sample_width,
    )
