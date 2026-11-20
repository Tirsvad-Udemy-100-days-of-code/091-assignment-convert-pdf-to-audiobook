"""@brief Convert a PDF file into an audiobook with text-to-speech.

This package follows a layered design: domain, application, infrastructure and
presentation.
"""

from pdf_to_audiobook.application.convert_pdf_to_audiobook import (
    convert_pdf_to_audiobook,
)

__all__ = ["__version__", "convert_pdf_to_audiobook"]

__version__ = "0.1.0"
