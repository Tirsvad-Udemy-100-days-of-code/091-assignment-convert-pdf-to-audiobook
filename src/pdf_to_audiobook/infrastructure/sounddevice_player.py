"""@brief Audio player that plays through the speakers with sounddevice."""

import io
import wave
from importlib import import_module
from typing import Any

from pdf_to_audiobook.constants import (
    PLAYBACK_INSTALL_COMMAND,
    PLAYBACK_SAMPLE_WIDTH,
)
from pdf_to_audiobook.domain.errors import PlaybackError
from pdf_to_audiobook.domain.speech import AudioClip


def _load_module(name: str) -> Any:  # Any: sounddevice has no type stubs
    """!@brief Import a playback package on first use.

    @param name Import name of the package.
    @return The imported module.
    @throws PlaybackError If the package is not installed.
    """
    try:
        return import_module(name)
    except ImportError as error:
        raise PlaybackError(
            f"Cannot play audio: {name} is not available. "
            f"Install it with: {PLAYBACK_INSTALL_COMMAND}"
        ) from error


def _read_samples(clip: AudioClip, numpy: Any) -> tuple[Any, int]:
    """!@brief Decode the WAV bytes of a clip into a sample array.

    @param clip The clip to decode.
    @param numpy The numpy module.
    @return The int16 samples shaped (frames, channels), and the sample rate.
    @throws PlaybackError If the clip is not a 16-bit WAV file.
    """
    try:
        with wave.open(io.BytesIO(clip.data), "rb") as reader:
            width = reader.getsampwidth()
            channels = reader.getnchannels()
            rate = reader.getframerate()
            frames = reader.readframes(reader.getnframes())
    except (wave.Error, EOFError) as error:
        raise PlaybackError(f"Cannot play audio: invalid WAV data: {error}") from error
    if width != PLAYBACK_SAMPLE_WIDTH:
        raise PlaybackError(
            f"Cannot play audio: only 16-bit WAV is supported, got {width * 8}-bit."
        )
    samples = numpy.frombuffer(frames, dtype=numpy.int16).reshape(-1, channels)
    return samples, rate


class SoundDevicePlayer:
    """!@brief AudioPlayer that plays clips through the default sound device."""

    def play(self, clip: AudioClip) -> None:
        """!@brief Play one clip and wait until it has finished.

        @param clip The 16-bit WAV clip to play.
        @return Nothing.
        @throws PlaybackError If the clip is not playable or the device fails.
        """
        sounddevice = _load_module("sounddevice")
        numpy = _load_module("numpy")
        samples, rate = _read_samples(clip, numpy)
        try:
            sounddevice.play(samples, rate)
            sounddevice.wait()
        except sounddevice.PortAudioError as error:
            raise PlaybackError(f"Cannot play audio: {error}") from error
