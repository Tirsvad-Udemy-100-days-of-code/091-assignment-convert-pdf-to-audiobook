# Quiet Console

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-008 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | Jens Tirsvad Nielsen | S01 | Initial version | [af93f22] |
| 2026-11-21 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-020]; stand-in for S01, not independent; plan accepted by S01 in chat | [af93f22] |

---

## Purpose

Decide whether the converter and the window run without the long phoneme text, download bars and library warnings of Coqui TTS on the console, while a `--verbose` flag brings that output back for diagnosis.

## Deliverable

An output-quieting wrapper around the model calls in the Coqui TTS adapter, a `--verbose` option on the command line and on the window, tests, and a short note in the README and the wiki (step 3, step 4 and step 6 pages in en, da and ms).

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | A real conversion of `tests/data/sample.pdf` without `--verbose` prints only the project's own lines (progress and `Wrote ...`) on stdout and stderr; the run is logged and the phoneme text, the `Character ... not found` warning and the download bars are absent | Met | Not met |
| 2 | With `--verbose` the library output is shown as before | Met | Not met |
| 3 | A real error of the engine (model fails to load or synthesize) is still shown as `error: ...` with exit code 1, and is never swallowed by the quieting | Met | Not met |
| 4 | The quieting is done in the infrastructure layer only; the domain and application layers do not change | Met | Not met |
| 5 | Tests with a fake model that prints to stdout, stderr and the `logging` module show that the output is hidden by default, is shown with the verbose flag, and that the streams are restored afterwards, also after an exception | Met | Not met |
| 6 | `pytest --cov` reports at least 90 % of the lines of `src/` and the opengrep scan, including the host scan, reports 0 error findings | Met | Not met |
| 7 | The README and the wiki pages for steps 3, 4 and 6 in en, da and ms mention `--verbose` | Met | Not met |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-003 | The Coqui TTS adapter |
| MIL-006 | The window options |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| BC-001 objective 1 (usable speech from text) | Success criterion 3 |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-22 — inside the Business Case constraint of 2026-11-20 to 2026-11-22.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Quiet the Coqui TTS output | In the infrastructure layer, run the model load and `tts_to_file` with stdout, stderr and the Coqui and torch loggers silenced unless verbose; always restore the streams and levels, also after an exception; keep real errors visible. | No | BC-001 objective 1 |
| 2 | Add the --verbose option | Add `--verbose` to the command line and to the window; pass it from the composition root to the engine; the domain and application layers stay unchanged. | No | BC-001 objective 1 |
| 3 | Write the tests | Test hidden by default, shown with verbose, errors kept, streams restored after an exception; coverage of at least 90 %. | No | Success criteria 2 to 6 |
| 4 | Make the real run | Convert the sample PDF with and without `--verbose` on the maintainer's machine and log both outputs. | No | Success criteria 1 and 2 |
| 5 | Scan and document | Run the opengrep scan, update the README and the wiki steps 3, 4 and 6 in en, da and ms. | No | Success criteria 6 and 7 |

---

[BC-001]: ../business-case.md
[RC-020]: ../sqa/reviews/rc-020-mil-008-quiet-console.md
[af93f22]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/af93f22d55f08dae087745bc41a00af2f4b93e60
