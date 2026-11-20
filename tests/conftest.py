from collections.abc import Callable
from pathlib import Path

import pytest

from tests.pdf_builder import build_pdf_bytes


@pytest.fixture
def make_pdf(tmp_path: Path) -> Callable[[list[str]], Path]:
    def _make(pages: list[str]) -> Path:
        path = tmp_path / "book.pdf"
        path.write_bytes(build_pdf_bytes(pages))
        return path

    return _make
