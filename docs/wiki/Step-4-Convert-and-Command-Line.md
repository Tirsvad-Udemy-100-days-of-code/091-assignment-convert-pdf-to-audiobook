**English** · [Dansk](Step-4-Convert-and-Command-Line-da) · [Bahasa Malaysia](Step-4-Convert-and-Command-Line-ms)

# Step 4: Convert and command line

![Step 4: convert a PDF to an audiobook](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-04-cli.svg)

## What we did

- `convert_pdf_to_audiobook(pdf_path, output_path, engine, extract_text, progress)` is the assignment's function: extract, split, speak each piece, join the clips and write one WAV file.
- `join_wav_clips` joins the clips with the standard library `wave` module and refuses clips with different audio settings.
- The command line is the composition root: it is the only place that builds the real engine and the real PDF reader.

```powershell
python -m pdf_to_audiobook tests/data/sample.pdf -o build/sample.wav
pdf-to-audiobook --help
```

Exit codes: 0 success, 1 an error with a message on stderr, 2 wrong use of the command.

## What we gained

- Dependencies point inward: the use case knows the port and a function, not Coqui TTS or `pypdf`.
- Progress and errors go to stderr and the result to stdout, so the program works in scripts.
- A real run on the two page sample PDF gave about 17 seconds of speech.
