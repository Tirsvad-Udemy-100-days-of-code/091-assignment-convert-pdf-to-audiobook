"""@brief Every constant of the project, defined once.

Other modules import their constants from here and never repeat the values.
"""

from typing import Final

## Import name of the package.
PACKAGE_NAME: Final[str] = "pdf_to_audiobook"
## Longest piece of text, in characters, sent to the speech engine at once.
MAX_CHUNK_CHARS: Final[int] = 400
## File name suffix of the audio the program writes.
AUDIO_FILE_SUFFIX: Final[str] = ".wav"

## Exit code when the work succeeded.
EXIT_OK: Final[int] = 0
## Exit code when the work failed.
EXIT_ERROR: Final[int] = 1
## Exit code when the command line was used wrongly.
EXIT_USAGE: Final[int] = 2
