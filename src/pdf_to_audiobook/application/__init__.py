"""@brief Application layer: use cases such as convert_pdf_to_audiobook.

It may import the domain layer only.
"""

from pdf_to_audiobook.application.convert_pdf_to_audiobook import (
    convert_pdf_to_audiobook,
)
from pdf_to_audiobook.application.speak_text import speak_text

__all__ = ["convert_pdf_to_audiobook", "speak_text"]
