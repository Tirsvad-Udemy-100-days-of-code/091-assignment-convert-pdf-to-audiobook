from collections.abc import Callable
from pathlib import Path

import pytest

from pdf_to_audiobook.domain.errors import AudiobookError, PdfTextError
from pdf_to_audiobook.infrastructure.pdf_reader import extract_text_from_pdf

MakePdf = Callable[[list[str]], Path]


def test_extract_returns_text_of_one_page(make_pdf: MakePdf) -> None:
    assert extract_text_from_pdf(make_pdf(["Hello (world)."])) == "Hello (world)."


def test_extract_joins_pages_in_order_with_blank_line(make_pdf: MakePdf) -> None:
    path = make_pdf(["First page.", "Second page.", "Third \\ page."])
    assert (
        extract_text_from_pdf(path) == "First page.\n\nSecond page.\n\nThird \\ page."
    )


def test_extract_accepts_str_and_path(make_pdf: MakePdf) -> None:
    path = make_pdf(["Same text."])
    assert extract_text_from_pdf(str(path)) == extract_text_from_pdf(path)


def test_extract_skips_empty_page_between_text_pages(make_pdf: MakePdf) -> None:
    assert extract_text_from_pdf(make_pdf(["A.", "", "B."])) == "A.\n\nB."


def test_extract_raises_for_missing_file(tmp_path: Path) -> None:
    with pytest.raises(PdfTextError, match="not found"):
        extract_text_from_pdf(tmp_path / "missing.pdf")


def test_extract_raises_for_file_that_is_not_a_pdf(tmp_path: Path) -> None:
    path = tmp_path / "fake.pdf"
    path.write_text("this is not a pdf", encoding="utf-8")
    with pytest.raises(PdfTextError, match="Cannot read"):
        extract_text_from_pdf(path)


def test_extract_raises_for_pdf_with_empty_page_only(make_pdf: MakePdf) -> None:
    with pytest.raises(PdfTextError, match="no text"):
        extract_text_from_pdf(make_pdf([""]))


def test_pdf_text_error_is_an_audiobook_error() -> None:
    assert issubclass(PdfTextError, AudiobookError)
