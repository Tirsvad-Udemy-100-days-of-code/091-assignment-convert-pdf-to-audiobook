"""@brief The view model of the speak window; it knows nothing of Tkinter."""

from collections.abc import Callable

from pdf_to_audiobook.application.speak_text import speak_text
from pdf_to_audiobook.constants import (
    STATUS_DONE,
    STATUS_ERROR_PREFIX,
    STATUS_READY,
    STATUS_SPEAKING,
)
from pdf_to_audiobook.domain.errors import AudiobookError
from pdf_to_audiobook.domain.speech import AudioPlayer, SpeechEngine


class SpeakViewModel:
    """!@brief The status and busy flag of the window, and the speak command."""

    def __init__(
        self,
        engine: SpeechEngine,
        player: AudioPlayer,
        on_change: Callable[[], None] | None = None,
    ) -> None:
        """!@brief Create the view model.

        @param engine The speech engine.
        @param player The audio player.
        @param on_change Called after status or busy changes; the view sets it.
        """
        ## The speech engine.
        self._engine = engine
        ## The audio player.
        self._player = player
        ## Called after status or busy changes.
        self.on_change = on_change
        ## Text shown to the user about the last or current action.
        self.status: str = STATUS_READY
        ## True while a text is being spoken.
        self.busy: bool = False

    def can_speak(self, text: str) -> bool:
        """!@brief Tell whether the Speak command is available.

        @param text The text in the text box.
        @return False while busy or when the text is blank.
        """
        return not self.busy and bool(text.strip())

    def speak(self, text: str) -> None:
        """!@brief Speak the text and update status and busy; blocks until done.

        An error of the program is shown as a status message, never raised.

        @param text The text to speak.
        @return Nothing.
        """
        self._update(STATUS_SPEAKING, busy=True)
        try:
            speak_text(text, self._engine, self._player)
        except AudiobookError as error:
            self._update(f"{STATUS_ERROR_PREFIX}{error}", busy=False)
        else:
            self._update(STATUS_DONE, busy=False)

    def _update(self, status: str, *, busy: bool) -> None:
        """!@brief Set status and busy, then tell the view.

        @param status The new status.
        @param busy The new busy flag.
        @return Nothing.
        """
        self.status = status
        self.busy = busy
        if self.on_change is not None:
            self.on_change()
