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

## Name of the Coqui TTS voice model the speech engine loads by default.
DEFAULT_MODEL_NAME: Final[str] = "tts_models/en/ljspeech/tacotron2-DCA"
## Name of the file the speech engine writes inside its temporary folder.
SPEECH_TEMP_FILE_NAME: Final[str] = "speech.wav"
## Command that installs the project and its speech engine.
INSTALL_COMMAND: Final[str] = "python -m pip install -e ."

## Exit code when the work succeeded.
EXIT_OK: Final[int] = 0
## Exit code when the work failed.
EXIT_ERROR: Final[int] = 1
## Exit code when the command line was used wrongly.
EXIT_USAGE: Final[int] = 2

## Pattern of a paragraph break: a blank line, with optional spaces on it.
PARAGRAPH_BREAK_PATTERN: Final[str] = r"\n\s*\n"
## Pattern of the whitespace after a sentence end (. ! or ?).
SENTENCE_BREAK_PATTERN: Final[str] = r"(?<=[.!?])\s+"
## Separator placed between the text of two pages.
PAGE_SEPARATOR: Final[str] = "\n\n"

## Name of the command line program.
PROGRAM_NAME: Final[str] = "pdf-to-audiobook"
## Description shown in the command line help.
PROGRAM_DESCRIPTION: Final[str] = "Convert a PDF file into an audiobook (WAV file)."
## Mode that opens a WAV file for reading.
WAV_READ_MODE: Final[str] = "rb"
## Mode that opens a WAV file for writing.
WAV_WRITE_MODE: Final[str] = "wb"

## Command that installs the audio playback package.
PLAYBACK_INSTALL_COMMAND: Final[str] = "python -m pip install sounddevice"
## Number of bytes per sample the player supports (16-bit audio).
PLAYBACK_SAMPLE_WIDTH: Final[int] = 2

## Name of the window program.
WINDOW_PROGRAM_NAME: Final[str] = "pdf-to-audiobook-window"
## Description shown in the window program help.
WINDOW_PROGRAM_DESCRIPTION: Final[str] = "Type text in a window and hear it spoken."
## Title of the window.
WINDOW_TITLE: Final[str] = "Speak text"
## Status shown before anything is spoken.
STATUS_READY: Final[str] = "Ready"
## Status shown while text is spoken.
STATUS_SPEAKING: Final[str] = "Speaking..."
## Status shown when speaking finished.
STATUS_DONE: Final[str] = "Done"
## Prefix of the status shown when speaking failed.
STATUS_ERROR_PREFIX: Final[str] = "error: "
