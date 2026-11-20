# Review Record: MIL-006 code

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-017 |
| CrossReference | [MIL-006], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Initial version; autonomous stand-in for S01, not independent | [359c357] |

---

## Artifact Under Review

- Instance reviewed: [MIL-006]
- Checklist used: [QC-PY-001]
- Scope: full review of `src/`, `tests/`, `tools/window_container_test.py`, `docker/` and `scripts/gui-test.ps1` of MIL-006
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is the author as stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Modules `speak_text`, `sounddevice_player`, `window`, `window_model`; classes `SoundDevicePlayer`, `SpeakViewModel`, `SpeakWindow`; constants in `UPPER_SNAKE`. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`speak_text`, `can_speak`, `PlaybackError`, `EmptyTextError`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff format` applied; `ruff check src tests tools` reports no finding; no suppression comment. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function is annotated; mypy strict passes on 19 source files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | Specific exceptions (`PortAudioError`, `ImportError`, `wave.Error`, `AudiobookError`, `TclError`) and `raise ... from`; the window shows the message, not a traceback. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default argument; no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | `wave.open` is used in a `with` block. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Public items have Doxygen docstrings; `doxygen Doxyfile` writes an empty warnings log after the fix of five member comments. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | The window prints only a start-up error to stderr, as the command line does; no logging, no secrets. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | N-A | No Design Class Diagram exists: plain technical tasks (see the Project Plan, Open Issues). |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 110 tests, 98 % coverage of `src`; the window runs in a container on a virtual display, with a log and a screenshot; no test makes a sound or uses the network. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy` strict reports no issue; the one `Any` (the lazily imported `sounddevice` module) has a comment. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `sounddevice~=0.5` is declared and pinned in `pyproject.toml` (ADR-0002); the console script is declared. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Chunk limit, window text and status strings are defined once in `constants.py`; the chunking is reused from the converter. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `application` imports only `domain`; `AudioPlayer` is a port in `domain`; `sounddevice`, Tkinter and Coqui TTS are imported only in `infrastructure` and `presentation`, and Tkinter and `sounddevice` lazily. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | One reason to change per module; the view model and the view are separate; the player and engine are narrow protocols injected in the composition root. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | New modules sit in `application`, `infrastructure` and `presentation`; tests are under `tests/unit`. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are English with letters, digits, `_` and `-`. |

## Overall Verdict

Go — no Mandatory criterion fails. The review is not independent: the author reviewed as stand-in for S01.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | 2026-11-20 |

---

[MIL-006]: ../../milestones/mil-006-speak-text-window.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[359c357]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/359c357f97c4df7626b2f192adeb4e44062597c4
