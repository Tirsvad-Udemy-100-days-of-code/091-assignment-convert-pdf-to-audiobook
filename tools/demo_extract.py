"""!@brief Show what the PDF reader and the text splitter do with a PDF file.

Usage::

    python tools/demo_extract.py tests/data/sample.pdf
"""

import sys
from pathlib import Path

from pdf_to_audiobook.domain.text_chunks import split_text_into_chunks
from pdf_to_audiobook.infrastructure.pdf_reader import extract_text_from_pdf


def main(argv: list[str]) -> int:
    """!@brief Print the extracted text and its chunks.

    @param argv Command line arguments: the path of the PDF file.
    @return Exit code, 0 on success and 2 when the path is missing.
    """
    if len(argv) != 1:
        print("usage: python tools/demo_extract.py <file.pdf>")
        return 2
    text = extract_text_from_pdf(Path(argv[0]))
    chunks = split_text_into_chunks(text)
    print(f"Extracted {len(text)} characters from {argv[0]}")
    print(f"Split into {len(chunks)} chunk(s):")
    for number, chunk in enumerate(chunks, start=1):
        print(f"  [{number}] {chunk}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
