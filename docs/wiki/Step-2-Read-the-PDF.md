**English** · [Dansk](Step-2-Read-the-PDF-da) · [Bahasa Malaysia](Step-2-Read-the-PDF-ms)

# Step 2: Read the PDF

![Step 2: read the PDF and split the text](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-02-extract-text.svg)

## What we did

- `extract_text_from_pdf` reads every page with `pypdf` and joins the page texts.
- `split_text_into_chunks` cuts the text at paragraph and sentence ends into pieces of at most 400 characters (`MAX_CHUNK_CHARS`), never in the middle of a word.
- A PDF with no text (for example a scan) gives a clear `PdfTextError` instead of silence.

```powershell
python tools/demo_extract.py tests/data/sample.pdf
```

## What we gained

- Speech engines work best with short pieces of text, so chunking is a real business rule, and it lives in the domain layer with no input or output.
- Tests need no binary files: a small standard-library function builds a valid PDF on the fly.
- Errors are named for what went wrong, and the original cause is kept with `raise ... from`.
