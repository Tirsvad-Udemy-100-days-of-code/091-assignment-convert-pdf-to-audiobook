# 🚀 PDF to Audiobook

A small Python program that reads a PDF file and turns its text into speech, so you get a free audiobook. It is the Day 91 assignment of the Udemy course *100 Days of Code: The Complete Python Pro Bootcamp*, for course participants and anyone who browses the repository for ideas.

## 📚 Table of Contents

- [Overview](#-overview)
- [Requirements](#-requirements)
- [Setup](#-setup)
- [Run](#-run)
- [Tests](#-tests)
- [License](#-license)
- [Links](#-links)
- [Appendix: Project documents](#-appendix-project-documents)

## 🧭 Overview

The program extracts the text of a PDF with `pypdf`, splits it into pieces of at most 400 characters and speaks each piece with [Coqui TTS][coqui], an open source speech engine that runs on your own machine. No paid service and no account are needed. The assignment's function is `convert_pdf_to_audiobook`.

| Folder | What it holds |
| --- | --- |
| `src/pdf_to_audiobook/` | The program, in layers: `domain`, `application`, `infrastructure`, `presentation`. All constants are in `constants.py` |
| `tests/` | pytest tests |
| `docs/` | Business case, plan, milestones, reviews, images and the wiki sources (`docs/wiki/`) |
| `scripts/` | The opengrep security scan and the window test in a container |
| `docker/` | The image and the script of the window test |
| `tools/` | `capture_step.py`, which renders command output as an SVG image for the documentation |

The project is built in six lecture steps. Each step has a screenshot below and a page in the [wiki][wiki] (English, Danish and Bahasa Malaysia) that explains what we gained.

### Step 1: Environment

![Step 1: create the .venv and upgrade pip][step-1]

### Step 2: Read the PDF

![Step 2: read the PDF and split the text][step-2]

### Step 3: Speak with Coqui TTS

![Step 3: speak a sentence with Coqui TTS][step-3]

### Step 4: Convert and command line

![Step 4: convert a PDF to an audiobook][step-4]

### Step 5: Tests and quality

![Step 5: run the tests][step-5]

### Step 6: The speak text window

![Step 6: the speak text window][step-6]

## 📋 Requirements

- Python 3.13 or newer, because the project targets it.
- `git`, to clone the repository.
- About 2 GB of free disk space and a few minutes: the project installs `pypdf`, Coqui TTS, PyTorch and `sounddevice`, and downloads a voice model (about 110 MB) on the first run. The speech engine runs on your own machine; no account and no paid service are needed.
- Optional for development: opengrep (`~/.opengrep/cli/latest/opengrep.exe`) for the security scan, and Doxygen for the API documentation.

## 🛠️ Setup

Create a local virtual environment, upgrade pip and install the project with the development tools.

Windows PowerShell:

```powershell
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook.git
cd 091-assignment-convert-pdf-to-audiobook
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux and macOS:

```bash
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook.git
cd 091-assignment-convert-pdf-to-audiobook
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The folder `.venv/` is ignored by git. Leave the environment with `deactivate`.

## ▶️ Run

With the virtual environment active, convert the sample PDF into a WAV file:

```powershell
python -m pdf_to_audiobook tests/data/sample.pdf -o build/sample.wav
```

The same program is installed as a command:

```powershell
pdf-to-audiobook my-book.pdf
pdf-to-audiobook my-book.pdf -o audio/my-book.wav --model tts_models/en/ljspeech/tacotron2-DCA
```

Without `-o` the audio is written next to the PDF with the suffix `.wav`. Exit code 0 means success, 1 an error (the message is on stderr) and 2 a wrong command line.

In Python the assignment's function is available as `convert_pdf_to_audiobook(pdf_path, output_path, engine, extract_text)`; see the [wiki][wiki] for the design.

### Speak typed text

Open a window, type text and press Speak to hear it through the speakers:

```powershell
pdf-to-audiobook-window
```

It uses the same voice model as the converter and plays the sound with `sounddevice`. On Linux install the system library `libportaudio2` first.

## 🧪 Tests

With the virtual environment active:

```powershell
python -m pytest
```

The real speech engine is tested by one slow test that is skipped by default and downloads the voice model on first use:

```powershell
python -m pytest -m slow
```

Check the code style and the types:

```powershell
python -m ruff check src tests
python -m mypy
```

The window is tested in a Linux container on a virtual display, never on your desktop (Docker is needed). The log and a screenshot go to `build/gui-results`:

```powershell
pwsh scripts/gui-test.ps1
```

Run the security scan before every push:

```powershell
pwsh scripts/scan.ps1
```

## 📄 License

GNU Affero General Public License v3, see [LICENSE][license].

## 🔗 Links

- [Repository][repository]
- [Documentation][documentation]
- [Issue tracker][issues]

## 📎 Appendix: Project documents

The documents a newcomer needs, in reading order.

| Document | What it tells you |
| --- | --- |
| [Business Case][BC-001] | Why the project exists, its scope and success criteria |
| [Stakeholder Analysis][SA-001] | Who is involved; the stakeholder IDs used for owners and reviewers |
| [Project Plan][PP-001] | The gateways and their schedule |
| [Milestones][milestones] | One document per gateway: Go/No-Go criteria and tasks |
| [Artifact registry][registry] | Where each artifact type lives, the next version, the PO language and domain |
| [Traceability matrix][TM-001] | How the artifacts link and when each was last reviewed |
| [Framework README][framework-readme] | The framework this project uses |
| [Framework changelog][framework-changelog] | What changed in each framework release |

---

[coqui]: https://github.com/idiap/coqui-ai-TTS
[license]: ./LICENSE
[repository]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook
[documentation]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/wiki
[issues]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/issues
[wiki]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/wiki
[step-1]: ./docs/images/step-01-setup.svg
[step-2]: ./docs/images/step-02-extract-text.svg
[step-3]: ./docs/images/step-03-coqui-tts.svg
[step-4]: ./docs/images/step-04-cli.svg
[step-5]: ./docs/images/step-05-tests.svg
[step-6]: ./docs/images/step-06-window.svg
[BC-001]: ./docs/business-case.md
[SA-001]: ./docs/stakeholder-analysis.md
[PP-001]: ./docs/project-plan.md
[milestones]: ./docs/milestones/
[registry]: ./docs/artifact-registry.md
[TM-001]: ./docs/sqa/traceability-matrix.md
[framework-readme]: ./framework/README.md
[framework-changelog]: ./framework/CHANGELOG.md
