import socket
from collections.abc import Callable
from pathlib import Path

import pytest

from tests.pdf_builder import build_pdf_bytes

NETWORK_BLOCKED_MESSAGE = "network access in a test"


@pytest.fixture(autouse=True)
def block_network(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Fail any test that opens a network connection, unless it is marked slow."""
    if request.node.get_closest_marker("slow") is not None:
        return

    def _blocked(*args: object, **kwargs: object) -> None:
        raise AssertionError(NETWORK_BLOCKED_MESSAGE)

    monkeypatch.setattr(socket.socket, "connect", _blocked)
    monkeypatch.setattr(socket, "create_connection", _blocked)


@pytest.fixture
def make_pdf(tmp_path: Path) -> Callable[[list[str]], Path]:
    def _make(pages: list[str]) -> Path:
        path = tmp_path / "book.pdf"
        path.write_bytes(build_pdf_bytes(pages))
        return path

    return _make
