import sys
import threading
import types
from collections.abc import Callable

import pytest
from tests.fakes import FakePlayer, FakeSpeechEngine

from pdf_to_audiobook.domain.errors import PlaybackError
from pdf_to_audiobook.presentation.window import main

WAIT_SECONDS = 5


class FakeWidget:
    """Stands in for a Tkinter widget; keeps the text and config it was given."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        self.options: dict[str, object] = dict(kwargs)
        self.content = ""
        self.command = kwargs.get("command")

    def pack(self, **kwargs: object) -> None:
        pass

    def bind(self, event: str, callback: Callable[[object], None]) -> None:
        pass

    def config(self, **kwargs: object) -> None:
        self.options.update(kwargs)

    def delete(self, start: str, end: str) -> None:
        self.content = ""

    def insert(self, index: str, text: str) -> None:
        self.content = text

    def get(self, start: str, end: str) -> str:
        return self.content + "\n"


class FakeTk:
    """Runs after() callbacks at once; mainloop waits until quit()."""

    created: list["FakeTk"] = []

    def __init__(self) -> None:
        self.stopped = threading.Event()
        self.destroyed = False
        FakeTk.created.append(self)

    def title(self, text: str) -> None:
        pass

    def after(self, delay: int, callback: Callable[[], None]) -> None:
        callback()

    def mainloop(self) -> None:
        assert self.stopped.wait(WAIT_SECONDS)

    def quit(self) -> None:
        self.stopped.set()

    def destroy(self) -> None:
        self.destroyed = True


class FakeTclError(Exception):
    pass


@pytest.fixture
def fake_tk(monkeypatch: pytest.MonkeyPatch) -> type[FakeTk]:
    module = types.ModuleType("tkinter")
    module.Tk = FakeTk  # type: ignore[attr-defined]
    module.Text = FakeWidget  # type: ignore[attr-defined]
    module.Button = FakeWidget  # type: ignore[attr-defined]
    module.Label = FakeWidget  # type: ignore[attr-defined]
    module.TclError = FakeTclError  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "tkinter", module)
    FakeTk.created.clear()
    return FakeTk


def test_main_script_speaks_the_text_and_exits_zero(fake_tk: type[FakeTk]) -> None:
    engine, player = FakeSpeechEngine(), FakePlayer()
    code = main(
        ["--script", "Hello there."],
        engine_factory=lambda _name: engine,
        player_factory=lambda: player,
    )
    assert code == 0
    assert engine.texts == ["Hello there."]
    assert len(player.clips) == 1
    assert fake_tk.created[0].destroyed


def test_main_script_exits_one_when_speaking_fails(fake_tk: type[FakeTk]) -> None:
    code = main(
        ["--script", "Hello there."],
        engine_factory=lambda _name: FakeSpeechEngine(),
        player_factory=lambda: FakePlayer(error=PlaybackError("no device")),
    )
    assert code == 1


def test_main_returns_one_when_no_display(
    fake_tk: type[FakeTk], monkeypatch: pytest.MonkeyPatch
) -> None:
    def _no_display(self: FakeTk) -> None:
        raise FakeTclError("no display")

    monkeypatch.setattr(FakeTk, "__init__", _no_display)
    code = main(
        [],
        engine_factory=lambda _name: FakeSpeechEngine(),
        player_factory=FakePlayer,
    )
    assert code == 1


def test_main_returns_two_for_unknown_option() -> None:
    assert main(["--nope"]) == 2


def test_main_returns_zero_for_help() -> None:
    assert main(["--help"]) == 0
