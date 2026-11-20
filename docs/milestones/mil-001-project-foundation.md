# Project Foundation

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Deprecated | Jens Tirsvad Nielsen | S01 | Initial version | [77d0001] |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-004]; stand-in for S01, not independent; language criteria confirmed by S01 in chat | [77d0001] |

---

## Purpose

Decide whether the repository skeleton and tooling are ready for code: Python 3.13 project, tests running, scan and documentation tooling in place.

## Deliverable

A repository with `pyproject.toml`, `src/` and `tests/` skeleton, `constants.py`, Python `.gitignore`, `.editorconfig`, Doxyfile, a first README, the opengrep scan procedure, repository description and topics on the git host, and the screenshot of lecture step 1 (environment setup).

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `pip install -e .[dev]` in a fresh `.venv` on Python 3.13 succeeds and `pytest` runs (one smoke test passes) | Met | Not met |
| 2 | `bash framework/scripts/check-editorconfig.sh` exits 0 | Met | Not met |
| 3 | `bash framework/scripts/check-readme.sh` exits 0 | Met | Not met |
| 4 | The opengrep scan of the branch reports 0 error findings | Met | Not met |
| 5 | The repository description and topics are set on the git host and read back through the API | Met | Not met |
| 6 | `docs/images/step-01-setup.svg` exists and is rendered from real command output | Met | Not met |

## Dependencies

| Depends on | Reason |
| --- | --- |
| none | First gateway |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| BC-001 objectives 4 and 5 | Success criteria 4 and 7 |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-20 — inside the Business Case constraint of 2026-11-20 to 2026-11-22.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Create the Python project skeleton | Add `pyproject.toml` (requires-python >=3.13, setuptools src layout, `pypdf` and Coqui TTS as the two dependencies, extra `dev` for pytest and pytest-cov, pytest settings), the package `pdf_to_audiobook` under `src/` with `constants.py` for every constant, and a smoke test under `tests/`. Layers follow the clean-architecture skill. | No | ADR-0001 |
| 2 | Add .gitignore and .editorconfig | Add a Python `.gitignore` that also ignores `.venv/`, `.env`, `.env.*`, audio output and `docs/ai-prompts/` when the repository is public; copy the framework baseline `.editorconfig` and check it with `check-editorconfig.sh`. | No | Framework rule 10 |
| 3 | Add Doxyfile and Doxygen comment style | Add a `Doxyfile` for `src/` that writes to `docs/doxygen/` (ignored by git) and document the Doxygen comment style used in the Python sources (`##` blocks with `@param`, `@return`, `@raises`). | No | BC-001 scope |
| 4 | Document the local .venv and pip upgrade | Write the setup steps for Windows PowerShell and POSIX shells: create `.venv`, activate it, run `python -m pip install --upgrade pip`, install the project with the `dev` extra (Coqui TTS is large and downloads a voice model on first use, so the README says so). Keep them in the first README, from the framework template, and check it with `check-readme.sh`. | No | CN-004 |
| 5 | Set up the opengrep scan before push | Write `scripts/scan.ps1` that runs `~\.opengrep\cli\latest\opengrep.exe` on the repository, settle which rule set works offline, and document that the scan runs before every push; record the result of each run in the pull request. | No | Success criterion 4 |
| 6 | Set repository description and topics | Using the git host API with the repository token read from the environment of the shell (never printed, never imported by the project, `.env` is not read by the code), set a short description and topics such as `python`, `pdf`, `text-to-speech`, `audiobook`, `pytest`, `udemy`, `100-days-of-code`, and read them back. | No | CN-005 |
| 7 | Add the screenshot tool and the step 1 screenshot | Write `tools/capture_step.py` (standard library only) that runs a command inside a container-free, non-GUI terminal capture and renders its real output as an SVG terminal image under `docs/images/`; produce `step-01-setup.svg` from the venv setup commands. No host desktop is used, so the GUI testing rule is not touched. | No | Success criterion 6 |
| 8 | Install git hooks and the plan gate | Run `install-git-hooks.sh --enable-plan-gate` so commits that change `src/` or `tests/` carry a `Task: MIL-NNN#N` trailer. | No | Plan-first gate |

---

[BC-001]: ../business-case.md
[RC-004]: ../sqa/reviews/rc-004-mil-001-project-foundation.md
[77d0001]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/77d0001724a50e0bcd2472de88d61f866cf9ece0
