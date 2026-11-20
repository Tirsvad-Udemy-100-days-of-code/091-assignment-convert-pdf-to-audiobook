"""!@brief Speak one sentence with Coqui TTS and report the audio that comes back.

The first run downloads the voice model (about 110 MB).

Usage::

    python tools/demo_speak.py "Hello from the audiobook."
"""

import sys
import tempfile
from pathlib import Path

from pdf_to_audiobook.infrastructure.coqui_engine import CoquiSpeechEngine


def main(argv: list[str]) -> int:
    """!@brief Synthesize the sentence and print the audio parameters.

    @param argv Command line arguments: the sentence to speak.
    @return Exit code, 0 on success and 2 when the sentence is missing.
    """
    if len(argv) != 1:
        print('usage: python tools/demo_speak.py "<sentence>"')
        return 2
    clip = CoquiSpeechEngine().synthesize(argv[0])
    seconds = len(clip.data) / (clip.sample_rate * clip.channels * clip.sample_width)
    with tempfile.TemporaryDirectory() as folder:
        target = Path(folder) / "speech.wav"
        target.write_bytes(clip.data)
        print(f"Wrote {target.stat().st_size} bytes of WAV audio")
    print(f"Sample rate {clip.sample_rate} Hz, channels {clip.channels}")
    print(f"About {seconds:.1f} seconds of speech")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
