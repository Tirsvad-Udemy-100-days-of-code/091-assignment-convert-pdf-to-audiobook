import io
import wave

from pdf_to_audiobook.domain.speech import AudioClip

FAKE_SAMPLE_RATE = 22050
FAKE_CHANNELS = 1
FAKE_SAMPLE_WIDTH = 2
FAKE_SECONDS = 0.1


def build_wav_bytes(
    sample_rate: int = FAKE_SAMPLE_RATE,
    channels: int = FAKE_CHANNELS,
    sample_width: int = FAKE_SAMPLE_WIDTH,
    seconds: float = FAKE_SECONDS,
) -> bytes:
    """Return a WAV file of silence."""
    frames = int(sample_rate * seconds)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as writer:
        writer.setnchannels(channels)
        writer.setsampwidth(sample_width)
        writer.setframerate(sample_rate)
        writer.writeframes(b"\x00" * frames * channels * sample_width)
    return buffer.getvalue()


class FakeSpeechEngine:
    """A SpeechEngine that returns silence and records the texts it got."""

    def __init__(self, error: Exception | None = None) -> None:
        self.texts: list[str] = []
        self._error = error

    def synthesize(self, text: str) -> AudioClip:
        self.texts.append(text)
        if self._error is not None:
            raise self._error
        return AudioClip(
            data=build_wav_bytes(),
            sample_rate=FAKE_SAMPLE_RATE,
            channels=FAKE_CHANNELS,
            sample_width=FAKE_SAMPLE_WIDTH,
        )
