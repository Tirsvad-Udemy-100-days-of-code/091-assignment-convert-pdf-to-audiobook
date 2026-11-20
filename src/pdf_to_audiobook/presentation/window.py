"""@brief Tkinter window that speaks typed text, and its composition root."""

import argparse
import sys
import threading
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from pdf_to_audiobook.constants import (
    DEFAULT_MODEL_NAME,
    EXIT_ERROR,
    EXIT_OK,
    EXIT_USAGE,
    STATUS_DONE,
    WINDOW_PROGRAM_DESCRIPTION,
    WINDOW_PROGRAM_NAME,
    WINDOW_TITLE,
)
from pdf_to_audiobook.domain.speech import AudioPlayer, SpeechEngine
from pdf_to_audiobook.infrastructure.coqui_engine import CoquiSpeechEngine
from pdf_to_audiobook.infrastructure.sounddevice_player import SoundDevicePlayer
from pdf_to_audiobook.presentation.window_model import SpeakViewModel

if TYPE_CHECKING:
    import tkinter as tk

## Milliseconds in a second, for the after() timers of Tkinter.
MILLISECONDS_PER_SECOND = 1000


class SpeakWindow:
    """!@brief The view: a text box, a Speak button and a status label."""

    def __init__(self, root: "tk.Tk", model: SpeakViewModel) -> None:
        """!@brief Build the widgets and bind them to the view model.

        @param root The Tk root window.
        @param model The view model.
        """
        import tkinter as tk  # Lazy: the package must import without a display.

        ## The Tk root window.
        self._root = root
        ## The view model.
        self._model = model
        ## Called on the main thread when a speak command has finished.
        self.on_finished: Callable[[], None] | None = None
        root.title(WINDOW_TITLE)
        ## The text box.
        self._text = tk.Text(root, width=60, height=10, wrap="word")
        self._text.pack(fill="both", expand=True, padx=8, pady=8)
        ## The Speak button.
        self._button = tk.Button(root, text="Speak", command=self.click_speak)
        self._button.pack(pady=4)
        ## The label that shows the status.
        self._status = tk.Label(root, anchor="w")
        self._status.pack(fill="x", padx=8, pady=4)
        ## Method called when the user types in the text box.
        self._text.bind("<KeyRelease>", self._on_key)
        model.on_change = self._schedule_refresh
        self.refresh()

    def set_text(self, text: str) -> None:
        """!@brief Replace the text in the text box.

        @param text The new text.
        @return Nothing.
        """
        self._text.delete("1.0", "end")
        self._text.insert("1.0", text)
        self.refresh()

    def speak_script(self, text: str) -> None:
        """!@brief Type a text into the box and press Speak.

        @param text The text to type.
        @return Nothing.
        """
        self.set_text(text)
        self.click_speak()

    def click_speak(self) -> None:
        """!@brief Start speaking the text on a worker thread.

        @return Nothing.
        """
        text = self._text.get("1.0", "end")
        if not self._model.can_speak(text):
            return
        self._button.config(state="disabled")
        threading.Thread(target=self._work, args=(text,), daemon=True).start()

    def refresh(self) -> None:
        """!@brief Show the status and enable the button as the model says.

        @return Nothing.
        """
        self._status.config(text=self._model.status)
        can_speak = self._model.can_speak(self._text.get("1.0", "end"))
        self._button.config(state="normal" if can_speak else "disabled")

    def _work(self, text: str) -> None:
        """!@brief Speak on the worker thread, then tell the main thread.

        @param text The text to speak.
        @return Nothing.
        """
        self._model.speak(text)
        ## Method posted to the main thread when speaking has ended.
        self._root.after(0, self._finish)

    def _on_key(self, _event: object) -> None:
        """!@brief Update the button after the user typed in the text box.

        @param _event The Tkinter key event; not used.
        @return Nothing.
        """
        self.refresh()

    def _schedule_refresh(self) -> None:
        """!@brief Post a refresh to the main thread; safe from any thread.

        @return Nothing.
        """
        ## Method posted to the main thread to update the widgets.
        self._root.after(0, self.refresh)

    def _finish(self) -> None:
        """!@brief Refresh after a finished command and call on_finished.

        @return Nothing.
        """
        self.refresh()
        if self.on_finished is not None:
            self.on_finished()


def main(
    argv: Sequence[str] | None = None,
    engine_factory: Callable[[str], SpeechEngine] | None = None,
    player_factory: Callable[[], AudioPlayer] | None = None,
) -> int:
    """!@brief Open the speak window.

    @param argv The arguments without the program name; defaults to sys.argv.
    @param engine_factory Builds an engine from a model name; defaults to Coqui.
    @param player_factory Builds the player; defaults to sounddevice.
    @return The exit code; in script mode 0 only if the speech ended as Done.
    """
    try:
        args = _build_parser().parse_args(argv)
    except SystemExit as exit_request:
        return EXIT_OK if exit_request.code in (0, None) else EXIT_USAGE
    engine = (engine_factory or CoquiSpeechEngine)(args.model)
    player = (player_factory or SoundDevicePlayer)()
    return _run_window(SpeakViewModel(engine, player), args.script, args.hold)


def _run_window(model: SpeakViewModel, script: str | None, hold: float) -> int:
    """!@brief Create the window and run its event loop.

    @param model The view model.
    @param script Text to type and speak automatically, or None for normal use.
    @param hold Seconds to keep the window open after a script has finished.
    @return The exit code.
    """
    import tkinter as tk  # Lazy: the package must import without a display.

    try:
        root = tk.Tk()
    except tk.TclError as error:
        print(f"error: cannot open a window: {error}", file=sys.stderr)
        return EXIT_ERROR
    window = SpeakWindow(root, model)
    if script is not None:
        delay = int(hold * MILLISECONDS_PER_SECOND)

        def quit_later() -> None:
            root.after(delay, root.quit)

        window.on_finished = quit_later
        root.after(0, lambda: window.speak_script(script))
    root.mainloop()
    root.destroy()
    if script is not None and model.status != STATUS_DONE:
        return EXIT_ERROR
    return EXIT_OK


def _build_parser() -> argparse.ArgumentParser:
    """!@brief Build the argument parser.

    @return The parser.
    """
    parser = argparse.ArgumentParser(
        prog=WINDOW_PROGRAM_NAME, description=WINDOW_PROGRAM_DESCRIPTION
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_NAME,
        help="Coqui TTS model name (default: %(default)s)",
    )
    parser.add_argument(
        "--script",
        help="type this text, speak it, and quit when done (for automated tests)",
    )
    parser.add_argument(
        "--hold",
        type=float,
        default=0.0,
        help="seconds to keep the window open after --script has finished",
    )
    return parser


if __name__ == "__main__":
    sys.exit(main())
