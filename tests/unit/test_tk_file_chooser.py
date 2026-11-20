import sys
import types
from pathlib import Path

import pytest

from pdf_to_audiobook.infrastructure.tk_file_chooser import TkFileChooser


def install_dialog(monkeypatch: pytest.MonkeyPatch, answer: str) -> dict[str, object]:
    received: dict[str, object] = {}

    def askopenfilename(**kwargs: object) -> str:
        received.update(kwargs)
        return answer

    module = types.ModuleType("tkinter")
    dialog = types.ModuleType("tkinter.filedialog")
    dialog.askopenfilename = askopenfilename  # type: ignore[attr-defined]
    module.filedialog = dialog  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "tkinter", module)
    monkeypatch.setitem(sys.modules, "tkinter.filedialog", dialog)
    return received


def test_choose_pdf_returns_the_chosen_path_limited_to_pdf(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    received = install_dialog(monkeypatch, "book.pdf")
    assert TkFileChooser().choose_pdf() == Path("book.pdf")
    assert received["filetypes"] == [("PDF files", "*.pdf")]


def test_choose_pdf_returns_none_when_cancelled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    install_dialog(monkeypatch, "")
    assert TkFileChooser().choose_pdf() is None
