"""@brief Errors the program raises on purpose."""


class AudiobookError(Exception):
    """@brief Base class of every error the program raises on purpose."""


class PdfTextError(AudiobookError):
    """@brief The text of a PDF file could not be read or is empty."""


class SpeechEngineError(AudiobookError):
    """@brief The speech engine could not turn text into audio."""


class EngineUnavailableError(SpeechEngineError):
    """@brief The speech engine is not installed or its model cannot be loaded."""


class AudioJoinError(AudiobookError):
    """!@brief Audio clips could not be joined or an audio file could not be written."""


class OutputWriteError(AudiobookError):
    """!@brief The audiobook file could not be written."""
