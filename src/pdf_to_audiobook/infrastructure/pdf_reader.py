"""@brief Read the text of a PDF file with pypdf."""

from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PyPdfError

from pdf_to_audiobook.constants import PAGE_SEPARATOR
from pdf_to_audiobook.domain.errors import PdfTextError


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """!@brief Read the text of every page of a PDF file.

    @param pdf_path Path of the PDF file.
    @return The page texts in order, joined by a blank line and stripped.
    @throws PdfTextError If the file is missing, unreadable or has no text.
    """
    path = Path(pdf_path)
    try:
        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
    except FileNotFoundError as error:
        raise PdfTextError(f"PDF file not found: {path}") from error
    except (PyPdfError, OSError) as error:
        raise PdfTextError(f"Cannot read PDF file {path}: {error}") from error
    text = PAGE_SEPARATOR.join(page.strip() for page in pages if page.strip())
    if not text:
        raise PdfTextError(f"PDF file has no text to read: {path}")
    return text
