"""@brief File chooser that shows the Tkinter open-file dialog."""

from pathlib import Path

from pdf_to_audiobook.constants import (
    FILE_DIALOG_TITLE,
    PDF_FILE_PATTERN,
    PDF_FILE_TYPE_LABEL,
)


class TkFileChooser:
    """!@brief FileChooser that opens the standard dialog, limited to PDF files."""

    def choose_pdf(self) -> Path | None:
        """!@brief Show the dialog and return the chosen file.

        @return The chosen path, or None when the user cancelled.
        """
        from tkinter import filedialog  # Lazy: no display is needed to import.

        name = filedialog.askopenfilename(
            title=FILE_DIALOG_TITLE,
            filetypes=[(PDF_FILE_TYPE_LABEL, PDF_FILE_PATTERN)],
        )
        return Path(name) if name else None
