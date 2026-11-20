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
| `docs/` | Business case, plan, milestones, reviews, images and the wiki |
| `scripts/` | The opengrep security scan |
| `tools/` | `capture_step.py`, which renders command output as an SVG image for the documentation |

The project is built step by step; each step has a screenshot in this README and a page in the wiki:

| Step | What it is | Screenshot |
| --- | --- | --- |
| 1 | Create the `.venv` and upgrade pip | ![Step 1][step-1] |

## 📋 Requirements

- Python 3.13 or newer, because the project targets it.
- `git`, to clone the repository.
- `pypdf`, installed with the project, to read PDF files.
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

Not available yet: the converter and the command line are added in a later step. This README is updated with the command when they exist.

## 🧪 Tests

With the virtual environment active:

```powershell
python -m pytest
```

Check the code style and the types:

```powershell
python -m ruff check src tests
python -m mypy
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
[step-1]: ./docs/images/step-01-setup.svg
[BC-001]: ./docs/business-case.md
[SA-001]: ./docs/stakeholder-analysis.md
[PP-001]: ./docs/project-plan.md
[milestones]: ./docs/milestones/
[registry]: ./docs/artifact-registry.md
[TM-001]: ./docs/sqa/traceability-matrix.md
[framework-readme]: ./framework/README.md
[framework-changelog]: ./framework/CHANGELOG.md
