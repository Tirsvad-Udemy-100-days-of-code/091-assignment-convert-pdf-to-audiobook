"""@brief The view model of the speak window; it knows nothing of Tkinter."""

import threading
from collections.abc import Callable
from pathlib import Path

from pdf_to_audiobook.application.speak_pdf import speak_pdf
from pdf_to_audiobook.application.speak_text import speak_text
from pdf_to_audiobook.constants import (
    STATUS_DONE,
    STATUS_ERROR_PREFIX,
    STATUS_LOADING,
    STATUS_READY,
    STATUS_SPEAKING,
    STATUS_SPEAKING_FILE_PREFIX,
    STATUS_STOPPED,
)
from pdf_to_audiobook.domain.errors import AudiobookError
from pdf_to_audiobook.domain.speech import AudioClip, AudioPlayer, SpeechEngine


class _ReportingEngine:
    """!@brief SpeechEngine that tells the view model after each synthesis."""

    def __init__(
        self, engine: SpeechEngine, on_synthesized: Callable[[], None]
    ) -> None:
        """!@brief Wrap an engine.

        @param engine The engine that does the work.
        @param on_synthesized Called after each clip has been synthesized.
        """
        ## The wrapped engine.
        self._engine = engine
        ## Called after each clip has been synthesized.
        self._on_synthesized = on_synthesized

    def synthesize(self, text: str) -> AudioClip:
        """!@brief Speak one piece of text through the wrapped engine.

        @param text The text to speak.
        @return The spoken text as a WAV clip.
        @throws SpeechEngineError If the text cannot be turned into audio.
        """
        clip = self._engine.synthesize(text)
        self._on_synthesized()
        return clip


class SpeakViewModel:
    """!@brief The status and busy flag of the window, and its commands."""

    def __init__(
        self,
        engine: SpeechEngine,
        player: AudioPlayer,
        extract_text: Callable[[Path], str],
        on_change: Callable[[], None] | None = None,
    ) -> None:
        """!@brief Create the view model.

        @param engine The speech engine.
        @param player The audio player.
        @param extract_text Function that returns the text of a PDF file.
        @param on_change Called after status or busy changes; the view sets it.
        """
        ## The speech engine; it reports back after each synthesis.
        self._engine: SpeechEngine = _ReportingEngine(engine, self._restore_speaking)
        ## The audio player.
        self._player = player
        ## Function that returns the text of a PDF file.
        self._extract_text = extract_text
        ## Set by stop(); read between two chunks.
        self._stop_requested = threading.Event()
        ## The status shown while speaking, without the loading phase.
        self._speaking_status = STATUS_SPEAKING
        ## Called after status or busy changes.
        self.on_change = on_change
        ## Text shown to the user about the last or current action.
        self.status: str = STATUS_READY
        ## True while a text or a PDF file is being spoken.
        self.busy: bool = False
        ## Every status that was set, in order.
        self.history: list[str] = [STATUS_READY]

    def can_speak(self, text: str) -> bool:
        """!@brief Tell whether the Speak command is available.

        @param text The text in the text box.
        @return False while busy or when the text is blank.
        """
        return not self.busy and bool(text.strip())

    def can_open(self) -> bool:
        """!@brief Tell whether the Open PDF command is available.

        @return False while busy.
        """
        return not self.busy

    def can_stop(self) -> bool:
        """!@brief Tell whether the Stop command is available.

        @return True only while busy.
        """
        return self.busy

    def speak(self, text: str) -> None:
        """!@brief Speak the text and update status and busy; blocks until done.

        An error of the program is shown as a status message, never raised.

        @param text The text to speak.
        @return Nothing.
        """
        self._run(
            STATUS_SPEAKING,
            lambda: speak_text(
                text, self._engine, self._player, should_stop=self._should_stop
            ),
        )

    def open_pdf(self, path: str | Path) -> None:
        """!@brief Speak a PDF file and update status and busy; blocks until done.

        The status shows the file name while speaking. An error of the program
        is shown as a status message, never raised.

        @param path Path of the PDF file.
        @return Nothing.
        """
        pdf_path = Path(path)
        self._run(
            f"{STATUS_SPEAKING_FILE_PREFIX}{pdf_path.name}",
            lambda: speak_pdf(
                pdf_path,
                self._engine,
                self._player,
                self._extract_text,
                should_stop=self._should_stop,
            ),
        )

    def notify_loading(self) -> None:
        """!@brief Show that the voice model is loading; called by the engine.

        Safe to call from a worker thread: the view posts its update to the
        main thread.

        @return Nothing.
        """
        self._update(STATUS_LOADING, busy=True)

    def stop(self) -> None:
        """!@brief Ask the running speech to end before its next chunk.

        @return Nothing.
        """
        if self.busy:
            self._stop_requested.set()

    def _should_stop(self) -> bool:
        """!@brief Tell whether stop() was called since the command began.

        @return True when the speech must end.
        """
        return self._stop_requested.is_set()

    def _run(self, speaking_status: str, command: Callable[[], int]) -> None:
        """!@brief Run a speaking command with status, busy and error handling.

        @param speaking_status The status shown while the command runs.
        @param command The command; it returns the number of chunks spoken.
        @return Nothing.
        """
        self._stop_requested.clear()
        self._speaking_status = speaking_status
        self._update(speaking_status, busy=True)
        try:
            command()
        except AudiobookError as error:
            self._update(f"{STATUS_ERROR_PREFIX}{error}", busy=False)
        else:
            stopped = self._stop_requested.is_set()
            self._update(STATUS_STOPPED if stopped else STATUS_DONE, busy=False)

    def _restore_speaking(self) -> None:
        """!@brief Show the speaking status again once the voice has loaded.

        @return Nothing.
        """
        if self.status == STATUS_LOADING:
            self._update(self._speaking_status, busy=True)

    def _update(self, status: str, *, busy: bool) -> None:
        """!@brief Set status and busy, then tell the view.

        @param status The new status.
        @param busy The new busy flag.
        @return Nothing.
        """
        self.status = status
        self.busy = busy
        self.history.append(status)
        if self.on_change is not None:
            self.on_change()
