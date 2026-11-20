import pytest

from pdf_to_audiobook.infrastructure.coqui_engine import CoquiSpeechEngine


@pytest.mark.slow
def test_real_engine_speaks_a_short_text() -> None:
    clip = CoquiSpeechEngine().synthesize("This is a short test.")
    assert clip.data.startswith(b"RIFF")
    assert clip.sample_rate > 0
