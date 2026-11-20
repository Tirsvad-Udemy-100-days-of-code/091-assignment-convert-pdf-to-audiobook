**English** · [Dansk](Home-da) · [Bahasa Malaysia](Home-ms)

# PDF to Audiobook

A small Python 3.13 program that reads a PDF file and turns its text into speech, so you get a free audiobook. It is the Day 91 assignment of the Udemy course *100 Days of Code: The Complete Python Pro Bootcamp*.

The assignment suggests paid text-to-speech web services. This project pays for nothing: it uses [Coqui TTS](https://github.com/idiap/coqui-ai-TTS), an open source speech engine that runs on your own machine.

## The five lecture steps

Each step has a page that shows a screenshot and explains what we gained.

| Step | Page | What it is |
| --- | --- | --- |
| 1 | [Step 1: Environment](Step-1-Environment) | A local `.venv`, pip upgraded, the project installed |
| 2 | [Step 2: Read the PDF](Step-2-Read-the-PDF) | Extract the text and split it into pieces |
| 3 | [Step 3: Speak with Coqui TTS](Step-3-Speak-with-Coqui-TTS) | Turn one piece of text into audio |
| 4 | [Step 4: Convert and command line](Step-4-Convert-and-Command-Line) | The whole conversion from a terminal |
| 5 | [Step 5: Tests and quality](Step-5-Tests-and-Quality) | Tests, types, style and the security scan |

Also read [Design](Design) for how the code is layered and [Reflection](Reflection) for what we learned.

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pdf_to_audiobook tests/data/sample.pdf -o build/sample.wav
```

The first install and the first run download several hundred megabytes (PyTorch and the voice model).
