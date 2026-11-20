# Business Case: PDF to Audiobook

## Metadata
| Key | Value |
| --- | --- |
| ID | BC-001 |
| CrossReference | [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Deprecated | Jens Tirsvad Nielsen | S01 | Initial version | [77d0001] |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-001]; stand-in for S01, not independent; language criteria confirmed by S01 in chat | [77d0001] |

---

## Executive Summary

Long documents are tiring to read. This project builds a small, readable Python 3.13 program that takes a PDF file, extracts its text and converts the text to speech, so that the user gets a free audiobook. It is the Day 91 assignment of a Python bootcamp course. The assignment suggests paid text-to-speech (TTS) web services; this project does not pay for any service, so it uses Coqui TTS, an open source engine that runs on the user's own machine. Tests use a test double of the speech engine, so they run fast and offline. The result is shared as a learning repository with a README and a three-language wiki.

## Methodological and Standards Foundation

The artifacts follow the SQA and QC framework mounted at `framework/`: Business Case, Stakeholder Analysis, Project Plan, milestones, then code, each step reviewed before the next. Quality is described with ISO/IEC 25010:2023 characteristics. The code follows Clean Architecture (domain rules do not import the HTTP client or the speech engine), the Python conventions of the `coding-conventions` skill, and Doxygen comments.

## Problem Statement

- Reading a long PDF takes time and attention that the reader does not always have.
- Free tools that read a PDF aloud are limited, and paid ones need an account.
- The assignment suggests paid TTS web services (iSpeech, Google Cloud, Amazon Polly). A repository that others clone cannot depend on a paid account, so they are not used.

## Business Opportunity

A free, scripted PDF-to-audio conversion shows how parsing, chunking and a neural speech engine fit together. The same repository is a teaching example for other course participants and for viewers of the public repository.

## Objectives

1. Provide a function `convert_pdf_to_audiobook` that turns a PDF file into an audio file.
2. Extract the text of a PDF page by page and split it into pieces the TTS service accepts.
3. Convert text to speech with Coqui TTS, the only speech engine, behind a small port so the engine can be replaced later.
4. Test every part with pytest, offline, using a test double of the speech engine; one optional slow test runs the real engine.
5. Document setup in a local `.venv`, how to run the program and the tests, and what each lecture step taught, in English, Danish and Bahasa Malaysia.

## Scope

### In Scope

- Python package under `src/` with a command line entry point.
- PDF text extraction, text chunking, Coqui TTS engine, audio file writing.
- pytest tests under `tests/` with a test double of the speech engine and one optional slow test of the real engine; constants in `constants.py`.
- `pyproject.toml`, Python `.gitignore`, `.editorconfig`, Doxyfile and Doxygen comments.
- README from the framework template and a wiki in en, da and ms, with a screenshot for each lecture step.
- Repository description and topics on the git host; an opengrep scan before each push.

### Out of Scope

- Any paid or hosted TTS service (iSpeech, Google Cloud TTS, Amazon Polly) and any other engine such as pyttsx3.
- Scanned PDFs that need OCR.
- A graphical user interface, packaging to PyPI and audio post-processing.
- Importing or testing the `.env` file: it holds personal tokens for the git host only.

## Expected Benefits

### Tangible Benefits

- A runnable program that converts a PDF to an audio file.
- A test suite that runs offline in seconds.
- A README and a three-language wiki that others can follow.

### Intangible Benefits

- Practice with a neural speech engine, ports and test doubles.
- A reflection that shows what was learned and what to improve next time.

## Strategic Alignment

The project supports the Product Owner's learning goal (Day 91 of the course) and the habit of keeping every step planned, reviewed and traceable through pull requests.

## Success Criteria

| # | Criterion | Target | Measure |
| --- | --- | --- | --- |
| 1 | Program converts a text PDF to audio | A sample PDF produces a non-empty audio file with the speech engine replaced by a test double | Test `test_convert_pdf_to_audiobook` passes |
| 2 | Default tests need no network, no paid account and no model download | 0 outbound requests during `pytest` | All default tests pass with sockets blocked |
| 3 | Test coverage of `src/` | At least 90 % of lines | `pytest --cov` report |
| 4 | Security scan is clean before each push | 0 findings of severity error | opengrep scan output, one per pull request |
| 5 | Documentation in three languages | Every English wiki page exists in `da` and `ms` | File list of `docs/wiki/` |
| 6 | One screenshot per lecture step | Each of the 5 steps has a screenshot in README and wiki | Image files under `docs/images/` |
| 7 | Runtime dependencies stay minimal | Exactly 2 required dependencies: `pypdf` and Coqui TTS | `pyproject.toml` dependencies list |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| The Coqui TTS project changes or stops | The engine stops working | The engine is behind a port, so a replacement is one class; versions are pinned in `pyproject.toml` |
| Coqui TTS is large, needs a model download on first run, or does not install on Python 3.13 | The program cannot speak | MIL-003 checks installation first; if it fails the run stops and reports, because the plan depends on it |
| PDF has no extractable text (scanned) | Empty audiobook | Report a clear error; OCR is out of scope |
| A secret leaks into the repository | Security incident | The program needs no key; `.env` is ignored; opengrep scan before push |
| Screenshots are tedious to produce by hand | Documentation is late | A script renders terminal output to images, run inside a container, not on the host desktop |

## Assumptions

- The user has Python 3.13 or newer and can create a virtual environment.
- Coqui TTS installs on Python 3.13 and its default English voice model can be downloaded once on the user's machine; MIL-003 verifies both before any engine code is written.
- The user's machine has enough disk space and memory for Coqui TTS and one voice model.
- The Product Owner is S01 and the reviewer is S01; in autonomous mode the reviews are made as a stand-in for S01, as described in `AGENTS.md`, so they are not independent.
- Course participants (S02) and repository viewers (S03) cannot be reached by the Product Owner during the project.

## Constraints

- Python 3.13 or newer; a `venv` in `.venv`; pytest; `pyproject.toml`; constants in `constants.py`.
- Source in `src/`, tests in `tests/`, documents in `docs/`.
- No paid or hosted services; the speech engine runs locally.
- Time: the assignment is planned for 150 minutes of course time; the repository work is planned for three days, 2026-11-20 to 2026-11-22.
- Runtime dependencies only where needed: `pypdf` and Coqui TTS (see ADR-0001).
- The word for artificial intelligence is not used in any artifact.
- Tokens are read from `.env` by the Product Owner's own tooling only; the project does not import, test or document its values.

## Cost–Benefit Assessment

| Costs | Benefits |
| --- | --- |
| About 3 days of the Product Owner's time and the stand-in's work; no licence cost; no hosting cost | A working, tested, documented example that is reusable by S02 and S03; qualitative only, because the project is a learning exercise and has no revenue |

## Stakeholders

| Stakeholder ID (SA) | Interest in this project |
| --- | --- |
| S01 | Owns the goal, develops, and reviews |
| S02 | Wants readable, runnable code with the assignment's function names and run instructions |
| S03 | Wants a clear description, topics and README, and no runtime dependencies |

## Recommendation

Proceed — the scope is small, free to run, and every part can be tested offline.

---

[SA-001]: ./stakeholder-analysis.md
[RC-001]: ./sqa/reviews/rc-001-business-case.md
[77d0001]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/77d0001724a50e0bcd2472de88d61f866cf9ece0
