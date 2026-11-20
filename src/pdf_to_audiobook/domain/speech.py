"""@brief The speech port and the audio it returns."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AudioClip:
    """!@brief A complete WAV file held in memory, with its parameters.

    @param data The bytes of the WAV file, header included.
    @param sample_rate Samples per second.
    @param channels Number of audio channels.
    @param sample_width Bytes per sample.
    """

    data: bytes
    sample_rate: int
    channels: int
    sample_width: int


class SpeechEngine(Protocol):
    """!@brief Turns a piece of text into spoken audio."""

    def synthesize(self, text: str) -> AudioClip:
        """!@brief Speak one piece of text.

        @param text The text to speak, not empty and within the chunk limit.
        @return The spoken text as a WAV clip.
        @throws SpeechEngineError If the text cannot be turned into audio.
        """
        ...
