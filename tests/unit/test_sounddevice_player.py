import sys
import types

import pytest
from tests.fakes import build_wav_bytes

from pdf_to_audiobook.domain.errors import PlaybackError
from pdf_to_audiobook.domain.speech import AudioClip
from pdf_to_audiobook.infrastructure.sounddevice_player import SoundDevicePlayer


class FakePortAudioError(Exception):
    pass


class FakeSoundDevice(types.ModuleType):
    PortAudioError = FakePortAudioError

    def __init__(self, fail: bool = False) -> None:
        super().__init__("sounddevice")
        self.played: list[tuple[int, tuple[int, ...], int]] = []
        self.waited = False
        self._fail = fail

    def play(self, samples: "object", rate: int) -> None:
        if self._fail:
            raise FakePortAudioError("no device")
        shape = tuple(samples.shape)
        self.played.append((len(shape), shape, rate))

    def wait(self) -> None:
        self.waited = True


def make_clip(channels: int = 1, sample_width: int = 2) -> AudioClip:
    return AudioClip(
        data=build_wav_bytes(channels=channels, sample_width=sample_width),
        sample_rate=22050,
        channels=channels,
        sample_width=sample_width,
    )


def test_play_sends_samples_to_the_device_and_waits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = FakeSoundDevice()
    monkeypatch.setitem(sys.modules, "sounddevice", fake)
    SoundDevicePlayer().play(make_clip(channels=2))
    assert fake.played == [(2, (2205, 2), 22050)]
    assert fake.waited


def test_play_maps_portaudio_error_to_playback_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "sounddevice", FakeSoundDevice(fail=True))
    with pytest.raises(PlaybackError, match="no device"):
        SoundDevicePlayer().play(make_clip())


def test_play_reports_missing_sounddevice(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "sounddevice", None)
    with pytest.raises(PlaybackError, match="pip install"):
        SoundDevicePlayer().play(make_clip())


def test_play_rejects_non_16_bit_audio(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "sounddevice", FakeSoundDevice())
    with pytest.raises(PlaybackError, match="16-bit"):
        SoundDevicePlayer().play(make_clip(sample_width=1))


def test_play_rejects_invalid_wav_data(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "sounddevice", FakeSoundDevice())
    clip = AudioClip(data=b"not a wav", sample_rate=22050, channels=1, sample_width=2)
    with pytest.raises(PlaybackError, match="invalid WAV"):
        SoundDevicePlayer().play(clip)
