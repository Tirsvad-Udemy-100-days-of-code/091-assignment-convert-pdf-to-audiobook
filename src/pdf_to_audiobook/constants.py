"""@brief Every constant of the project, defined once.

Other modules import their constants from here and never repeat the values.
"""

from typing import Final

PACKAGE_NAME: Final[str] = "pdf_to_audiobook"
MAX_CHUNK_CHARS: Final[int] = 400
AUDIO_FILE_SUFFIX: Final[str] = ".wav"

EXIT_OK: Final[int] = 0
EXIT_ERROR: Final[int] = 1
EXIT_USAGE: Final[int] = 2
