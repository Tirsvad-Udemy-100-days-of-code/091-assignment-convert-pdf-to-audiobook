import sys
import threading
import types
from collections.abc import Callable
from pathlib import Path

import pytest
from tests.fakes import (
    FakeFileChooser,
    FakePlayer,
    FakeSpeechEngine,
    FakeTtsLoader,
)

from pdf_to_audiobook.domain.errors import EngineUnavailableError, PlaybackError
from pdf_to_audiobook.presentation import window
from pdf_to_audiobook.presentation.window import SpeakWindow, main
from pdf_to_audiobook.presentation.window_model import SpeakViewModel

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
    module.Frame = FakeWidget  # type: ignore[attr-defined]
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


def run_open_pdf(chooser: FakeFileChooser, player: FakePlayer) -> int:
    return main(
        ["--open-pdf"],
        engine_factory=lambda _name: FakeSpeechEngine(),
        player_factory=lambda: player,
        chooser_factory=lambda: chooser,
    )


def test_main_open_pdf_speaks_the_chosen_file(
    fake_tk: type[FakeTk], make_pdf: Callable[[list[str]], Path]
) -> None:
    player = FakePlayer()
    code = run_open_pdf(FakeFileChooser(make_pdf(["One.", "Two."])), player)
    assert code == 0
    assert len(player.clips) == 2


def test_main_open_pdf_exits_one_when_the_dialog_is_cancelled(
    fake_tk: type[FakeTk],
) -> None:
    chooser = FakeFileChooser(None)
    assert run_open_pdf(chooser, FakePlayer()) == 1
    assert chooser.asked == 1


def test_main_open_pdf_exits_one_for_a_missing_file(
    fake_tk: type[FakeTk], tmp_path: Path
) -> None:
    code = run_open_pdf(FakeFileChooser(tmp_path / "missing.pdf"), FakePlayer())
    assert code == 1


def test_window_stop_and_key_events_refresh_without_error(
    fake_tk: type[FakeTk],
) -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(), lambda _path: "x")
    window = SpeakWindow(FakeTk(), model, FakeFileChooser(None))
    window.click_stop()
    window._on_key(None)
    assert not window.click_speak()
    assert not window.click_open()


def test_main_returns_zero_when_the_user_already_closed_the_window(
    fake_tk: type[FakeTk], monkeypatch: pytest.MonkeyPatch
) -> None:
    def _already_destroyed(self: FakeTk) -> None:
        raise FakeTclError("application has been destroyed")

    monkeypatch.setattr(FakeTk, "destroy", _already_destroyed)
    monkeypatch.setattr(FakeTk, "mainloop", lambda self: None)
    code = main(
        [],
        engine_factory=lambda _name: FakeSpeechEngine(),
        player_factory=FakePlayer,
    )
    assert code == 0


@pytest.mark.parametrize("error", [FakeTclError("destroyed"), RuntimeError("loop")])
def test_late_worker_update_after_close_does_not_raise(
    fake_tk: type[FakeTk], monkeypatch: pytest.MonkeyPatch, error: Exception
) -> None:
    model = SpeakViewModel(FakeSpeechEngine(), FakePlayer(), lambda _path: "x")
    root = FakeTk()
    SpeakWindow(root, model, FakeFileChooser(None))

    def _closed(self: FakeTk, delay: int, callback: Callable[[], None]) -> None:
        raise error

    monkeypatch.setattr(FakeTk, "after", _closed)
    model.speak("Hello there.")
    assert model.status == "Done"


@pytest.mark.parametrize(("flags", "expected"), [([], False), (["--verbose"], True)])
def test_main_passes_verbose_to_the_default_engine(
    fake_tk: type[FakeTk],
    monkeypatch: pytest.MonkeyPatch,
    flags: list[str],
    expected: bool,
) -> None:
    seen: list[bool] = []

    class StubEngine(FakeSpeechEngine):
        def __init__(self, model_name: str, verbose: bool, **options: object) -> None:
            super().__init__()
            seen.append(verbose)

    monkeypatch.setattr(window, "CoquiSpeechEngine", StubEngine)
    code = main([*flags, "--script", "Hello there."], player_factory=FakePlayer)
    assert code == 0
    assert seen == [expected]


def test_main_default_engine_reports_loading_through_the_window(
    fake_tk: type[FakeTk],
) -> None:
    models: list[SpeakViewModel] = []
    loader = FakeTtsLoader()
    code = main(
        ["--script", "Hello there."],
        player_factory=FakePlayer,
        tts_loader=loader,
        on_model=models.append,
    )
    assert code == 0
    assert loader.calls == 1
    assert models[0].history == [
        "Ready",
        "Speaking...",
        "Loading voice...",
        "Speaking...",
        "Done",
    ]


def test_main_shows_load_failure_as_error(fake_tk: type[FakeTk]) -> None:
    models: list[SpeakViewModel] = []
    loader = FakeTtsLoader(error=EngineUnavailableError("no model"))
    code = main(
        ["--script", "Hello there."],
        player_factory=FakePlayer,
        tts_loader=loader,
        on_model=models.append,
    )
    assert code == 1
    assert models[0].status == "error: no model"
    assert not models[0].busy
