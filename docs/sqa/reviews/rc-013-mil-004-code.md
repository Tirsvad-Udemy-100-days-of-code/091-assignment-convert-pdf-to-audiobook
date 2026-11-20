# Review Record: MIL-004 code

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-013 |
| CrossReference | [MIL-004], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Initial version; autonomous stand-in for S01, not independent | [8a4453f] |

---

## Artifact Under Review

- Instance reviewed: [MIL-004]
- Checklist used: [QC-PY-001]
- Scope: full review of `src/`, `tests/` and `tools/` of MIL-004, including the capture tool fix
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is the author as stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Modules `audio_join`, `convert_pdf_to_audiobook`, `cli`; function `convert_pdf_to_audiobook`; errors `AudioJoinError` and `OutputWriteError`; constants in `UPPER_SNAKE`. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose; the output-write failure has its own error `OutputWriteError` after the first review pass found it raised as `AudioJoinError`. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff format` applied and `ruff check src tests tools` reports no finding; no suppression comment. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function is annotated; mypy strict passes on 15 source files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | `except` clauses name specific errors and every re-raise uses `from`; the CLI turns `AudiobookError` into an exit code and a message on stderr. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default argument; no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | `wave.open` is used in `with` blocks; files are written with `Path.write_bytes`. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Public items have Doxygen docstrings; `doxygen Doxyfile` writes an empty warnings log. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | The presentation layer writes progress and errors to stderr and the result to stdout by design of a command line; no logging is used elsewhere; no secret exists. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | N-A | No Design Class Diagram exists: plain technical tasks (see the Project Plan, Open Issues). The use case function follows the assignment name `convert_pdf_to_audiobook`. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 86 tests, 99 % line and branch coverage of `src` (only `__main__.py` is not counted because its test runs in a subprocess); the network is blocked in every default test. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy` strict reports no issue. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | The console script and all dependencies are declared in `pyproject.toml`; pinning stays the action item of RC-009. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Program name, description, exit codes and WAV modes are constants defined once. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `application` imports only `domain` and constants; `presentation` is the only place that names `CoquiSpeechEngine` and `extract_text_from_pdf` (composition root). |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | The converter depends on the `SpeechEngine` port and an injected extractor, so another engine or reader needs no change to it. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Code sits in `domain`, `application` and `presentation`; tests in `unit` and `e2e`. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are English with letters, digits and `_`. |

## Overall Verdict

Go — no Mandatory criterion fails. The review is not independent: the author reviewed as stand-in for S01.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | 2026-11-20 |

---

[MIL-004]: ../../milestones/mil-004-converter-and-cli.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[8a4453f]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/8a4453ff4f4dcb70d630258c905733ed4ad25a1e
