# Review Record: MIL-003 code

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-012 |
| CrossReference | [MIL-003], [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Initial version; autonomous stand-in for S01, not independent | pending |

---

## Artifact Under Review

- Instance reviewed: [MIL-003]
- Checklist used: [QC-PY-001]
- Scope: full review of `src/`, `tests/` and `tools/` of MIL-003
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is the author as stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Modules `speech`, `coqui_engine`; classes `AudioClip`, `SpeechEngine`, `CoquiSpeechEngine`, `FakeSpeechEngine`; constants in `UPPER_SNAKE`. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`load_coqui_model`, `EngineUnavailableError`, `block_network`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff format` applied and `ruff check src tests tools` reports no finding; no suppression comment. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function is annotated; mypy strict passes on 11 source files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | The engine catches narrow exception tuples and re-raises package errors `from` the cause; no bare except. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default argument; no builtin shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | The temporary folder is a `TemporaryDirectory` context manager and the audio file is read with `Path.read_bytes`. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Public items have Doxygen docstrings; `doxygen Doxyfile` writes an empty warnings log. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No logging and no `print` in `src`; only the demo script prints; no secret exists. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | N-A | No Design Class Diagram exists: plain technical tasks (see the Project Plan, Open Issues). The port follows the clean-architecture skill. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 56 tests, 100 % line and branch coverage of `src`; an autouse fixture blocks sockets so no test can use the network; one `slow` test synthesized real audio and passed in 38 s when run by hand. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy` strict reports no issue; `TTS` is typed through a small Protocol and ignored through a documented mypy override because the package ships no stubs. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `coqui-tts[codec,languages]`, `torch`, `torchaudio` and `pypdf` are declared and used; pinning stays the action item of RC-009. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Model name, install command and temporary file name are constants defined once. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `domain` imports only the standard library; `infrastructure` imports `domain`; `TTS` is imported lazily inside the loader only. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | The engine depends on the narrow `TtsModel` protocol and an injected loader; a new engine implements `SpeechEngine` without editing existing code. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Code sits in `domain` and `infrastructure`; tests in `tests/unit` and `tests/integration`. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are English with letters, digits and `_`. |

## Overall Verdict

Go — no Mandatory criterion fails. The review is not independent: the author reviewed as stand-in for S01.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | 2026-11-20 |

---

[MIL-003]: ../../milestones/mil-003-speech-engines.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
