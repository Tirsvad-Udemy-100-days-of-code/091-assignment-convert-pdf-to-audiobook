"""@brief Errors the program raises on purpose."""


class AudiobookError(Exception):
    """@brief Base class of every error the program raises on purpose."""


class PdfTextError(AudiobookError):
    """@brief The text of a PDF file could not be read or is empty."""
