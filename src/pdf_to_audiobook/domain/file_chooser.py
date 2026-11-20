"""@brief The port that lets the user choose a file."""

from pathlib import Path
from typing import Protocol


class FileChooser(Protocol):
    """!@brief Asks the user to choose a PDF file."""

    def choose_pdf(self) -> Path | None:
        """!@brief Ask the user for a PDF file.

        @return The chosen path, or None when the user cancelled.
        """
        ...
