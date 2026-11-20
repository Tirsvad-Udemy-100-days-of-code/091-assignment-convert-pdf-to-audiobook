**English** · [Dansk](Step-7-Open-PDF-in-the-Window-da) · [Bahasa Malaysia](Step-7-Open-PDF-in-the-Window-ms)

# Step 7: Open a PDF in the window

![Step 7: open a PDF and hear it](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-07-open-pdf.svg)

## What we did

- We added an Open PDF button and a Stop button to the window. Open PDF shows a file dialog for PDF files, reads the text with `pypdf` and speaks it page by page through the speakers.
- `speak_pdf(pdf_path, engine, player, extract_text)` is the use case. The text extractor and the file chooser are injected, so the use case never imports `pypdf` or Tkinter and tests pick a file without a dialog.
- `speak_text` and `speak_pdf` share one loop, `speak_chunks`, so the rule "check for Stop, speak a chunk, play it" exists once. Stop ends the speech between two chunks.
- A missing, unreadable or empty PDF is shown as a message in the status line, not as a traceback.

```powershell
pdf-to-audiobook-window
pwsh scripts/gui-test.ps1
```

- The container test opens `tests/data/sample.pdf` through a fake file chooser on a virtual display and reaches the status Done (`pwsh scripts/gui-test.ps1`). The screenshot above comes from it.
- One real run spoke the sample PDF through the speakers: 2 chunks, 23 seconds, exit code 0.

## What we gained

- Injecting the extractor and the chooser kept the window testable: only the real run needs a dialog and a sound card.
- Sharing one loop between typed text and PDF text meant that Stop worked for both with one change.
- `pypdf` is imported only when a PDF is opened, so the window starts fast and the container needs it only for this test.
