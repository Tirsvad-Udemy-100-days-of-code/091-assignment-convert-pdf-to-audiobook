"""@brief Tkinter window that speaks typed text or a PDF file, and its root."""

import argparse
import sys
import threading
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Literal

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
from pdf_to_audiobook.domain.file_chooser import FileChooser
from pdf_to_audiobook.domain.speech import AudioPlayer, SpeechEngine
from pdf_to_audiobook.infrastructure.coqui_engine import CoquiSpeechEngine
from pdf_to_audiobook.infrastructure.sounddevice_player import SoundDevicePlayer
from pdf_to_audiobook.infrastructure.tk_file_chooser import TkFileChooser
from pdf_to_audiobook.presentation.window_model import SpeakViewModel

if TYPE_CHECKING:
    import tkinter as tk

## Milliseconds in a second, for the after() timers of Tkinter.
MILLISECONDS_PER_SECOND = 1000


class SpeakWindow:
    """!@brief The view: a text box, three buttons and a status label."""

    def __init__(
        self, root: "tk.Tk", model: SpeakViewModel, chooser: FileChooser
    ) -> None:
        """!@brief Build the widgets and bind them to the view model.

        @param root The Tk root window.
        @param model The view model.
        @param chooser Lets the user choose a PDF file.
        """
        import tkinter as tk  # Lazy: the package must import without a display.

        ## The Tk root window.
        self._root = root
        ## The view model.
        self._model = model
        ## Lets the user choose a PDF file.
        self._chooser = chooser
        ## Called on the main thread when a speak command has finished.
        self.on_finished: Callable[[], None] | None = None
        root.title(WINDOW_TITLE)
        ## The text box.
        self._text = tk.Text(root, width=60, height=10, wrap="word")
        self._text.pack(fill="both", expand=True, padx=8, pady=8)
        ## The row that holds the buttons.
        self._buttons = tk.Frame(root)
        self._buttons.pack(pady=4)
        ## The Speak button.
        self._button = self._add_button("Speak", self.click_speak)
        ## The Open PDF button.
        self._open_button = self._add_button("Open PDF", self.click_open)
        ## The Stop button.
        self._stop_button = self._add_button("Stop", self.click_stop)
        ## The label that shows the status.
        self._status = tk.Label(root, anchor="w")
        self._status.pack(fill="x", padx=8, pady=4)
        ## Method called when the user types in the text box.
        self._text.bind("<KeyRelease>", self._on_key)
        model.on_change = self._schedule_refresh
        self.refresh()

    def _add_button(self, label: str, command: Callable[[], object]) -> "tk.Button":
        """!@brief Create one button in the button row.

        @param label The text on the button.
        @param command Called when the button is pressed.
        @return The button.
        """
        import tkinter as tk  # Lazy: the package must import without a display.

        button = tk.Button(self._buttons, text=label, command=command)
        button.pack(side="left", padx=4)
        return button

    def set_text(self, text: str) -> None:
        """!@brief Replace the text in the text box.

        @param text The new text.
        @return Nothing.
        """
        self._text.delete("1.0", "end")
        self._text.insert("1.0", text)
        self.refresh()

    def run_script(self, text: str, open_pdf: bool) -> bool:
        """!@brief Type a text into the box and press Speak or Open PDF.

        @param text The text to type.
        @param open_pdf True to press Open PDF, False to press Speak.
        @return True when speaking started.
        """
        self.set_text(text)
        return self.click_open() if open_pdf else self.click_speak()

    def click_speak(self) -> bool:
        """!@brief Start speaking the text on a worker thread.

        @return True when speaking started.
        """
        text = self._text.get("1.0", "end")
        if not self._model.can_speak(text):
            return False
        self._start(self._model.speak, text)
        return True

    def click_open(self) -> bool:
        """!@brief Ask for a PDF file and start speaking it on a worker thread.

        @return True when speaking started; False if busy or cancelled.
        """
        if not self._model.can_open():
            return False
        path = self._chooser.choose_pdf()
        if path is None:
            return False
        self._start(self._model.open_pdf, str(path))
        return True

    def click_stop(self) -> None:
        """!@brief Ask the running speech to stop.

        @return Nothing.
        """
        self._model.stop()
        self.refresh()

    def _start(self, command: Callable[[str], None], argument: str) -> None:
        """!@brief Disable the buttons and run a command on a worker thread.

        @param command The view model command to run.
        @param argument The argument of the command.
        @return Nothing.
        """
        self._button.config(state="disabled")
        self._open_button.config(state="disabled")
        threading.Thread(
            target=self._work, args=(command, argument), daemon=True
        ).start()

    def refresh(self) -> None:
        """!@brief Show the status and enable the buttons as the model says.

        @return Nothing.
        """
        self._status.config(text=self._model.status)
        can_speak = self._model.can_speak(self._text.get("1.0", "end"))
        self._button.config(state=_state(can_speak))
        self._open_button.config(state=_state(self._model.can_open()))
        self._stop_button.config(state=_state(self._model.can_stop()))

    def _work(self, command: Callable[[str], None], argument: str) -> None:
        """!@brief Run a command on the worker thread, then tell the main thread.

        @param command The view model command to run.
        @param argument The argument of the command.
        @return Nothing.
        """
        command(argument)
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


def _state(is_enabled: bool) -> Literal["normal", "disabled"]:
    """!@brief Translate a flag to a Tkinter widget state.

    @param is_enabled True for an enabled widget.
    @return "normal" or "disabled".
    """
    return "normal" if is_enabled else "disabled"


def _extract_text(pdf_path: Path) -> str:
    """!@brief Read a PDF file; pypdf is imported on the first call only.

    @param pdf_path Path of the PDF file.
    @return The text of the PDF file.
    @throws PdfTextError If the text cannot be read.
    """
    from pdf_to_audiobook.infrastructure.pdf_reader import extract_text_from_pdf

    return extract_text_from_pdf(pdf_path)


def main(
    argv: Sequence[str] | None = None,
    engine_factory: Callable[[str], SpeechEngine] | None = None,
    player_factory: Callable[[], AudioPlayer] | None = None,
    chooser_factory: Callable[[], FileChooser] | None = None,
) -> int:
    """!@brief Open the speak window.

    @param argv The arguments without the program name; defaults to sys.argv.
    @param engine_factory Builds an engine from a model name; defaults to Coqui.
    @param player_factory Builds the player; defaults to sounddevice.
    @param chooser_factory Builds the file chooser; defaults to the Tk dialog.
    @return The exit code; in script mode 0 only if the speech ended as Done.
    """
    try:
        args = _build_parser().parse_args(argv)
    except SystemExit as exit_request:
        return EXIT_OK if exit_request.code in (0, None) else EXIT_USAGE
    engine = (engine_factory or CoquiSpeechEngine)(args.model)
    player = (player_factory or SoundDevicePlayer)()
    chooser = (chooser_factory or TkFileChooser)()
    model = SpeakViewModel(engine, player, _extract_text)
    script = args.script
    if script is None and args.open_pdf:
        script = ""
    return _run_window(model, chooser, script, args.open_pdf, args.hold)


def _run_window(
    model: SpeakViewModel,
    chooser: FileChooser,
    script: str | None,
    open_pdf: bool,
    hold: float,
) -> int:
    """!@brief Create the window and run its event loop.

    @param model The view model.
    @param chooser Lets the user choose a PDF file.
    @param script Text to type and speak automatically, or None for normal use.
    @param open_pdf True to press Open PDF automatically instead of Speak.
    @param hold Seconds to keep the window open after a script has finished.
    @return The exit code.
    """
    import tkinter as tk  # Lazy: the package must import without a display.

    try:
        root = tk.Tk()
    except tk.TclError as error:
        print(f"error: cannot open a window: {error}", file=sys.stderr)
        return EXIT_ERROR
    window = SpeakWindow(root, model, chooser)
    if script is not None:
        delay = int(hold * MILLISECONDS_PER_SECOND)

        def quit_later() -> None:
            root.after(delay, root.quit)

        window.on_finished = quit_later

        def start_script() -> None:
            if not window.run_script(script, open_pdf):
                root.quit()

        root.after(0, start_script)
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
        "--open-pdf",
        action="store_true",
        help="press Open PDF, speak the chosen file, and quit when done "
        "(for automated tests)",
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
