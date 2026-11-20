# Converter and Command Line

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-004 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Deprecated | Jens Tirsvad Nielsen | S01 | Initial version | pending |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-007]; stand-in for S01, not independent; language criteria confirmed by S01 in chat | pending |

---

## Purpose

Decide whether the whole conversion works end to end from the command line.

## Deliverable

`convert_pdf_to_audiobook`, the audio joining, the command line (`python -m pdf_to_audiobook` and a console script), an end-to-end test, and the screenshots of lecture steps 4 and 5.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | An end-to-end test converts a generated PDF to an audio file that is non-empty and has the expected format, with the speech engine replaced by the test double | Met | Not met |
| 2 | `python -m pdf_to_audiobook --help` lists the options and exits 0; a missing file exits with a non-zero code and a readable message | Met | Not met |
| 3 | WAV clips are joined with the standard library `wave` module into one valid WAV file, and clips with different audio parameters are rejected with a clear error | Met | Not met |
| 4 | `pytest --cov` reports at least 90 % of the lines of `src/` | Met | Not met |
| 5 | The opengrep scan of the branch reports 0 error findings | Met | Not met |
| 6 | `docs/images/step-04-cli.svg` and `docs/images/step-05-tests.svg` exist | Met | Not met |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-003 | The converter uses the engines |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| BC-001 objectives 1, 3 and 4 | Success criteria 1, 2, 3 |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-21 — inside the Business Case constraint of 2026-11-20 to 2026-11-22.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Implement the audio joiner | Join WAV `AudioClip` objects with the `wave` module; reject clips whose channels, sample width or sample rate differ. | No | BC-001 objective 1 |
| 2 | Implement convert_pdf_to_audiobook | Provide `convert_pdf_to_audiobook(pdf_path, output_path, engine)` with the assignment function name: extract, chunk, synthesize each chunk, join and write the file; report progress through a callback. | No | BC-001 objective 1 |
| 3 | Implement the command line | Add `argparse` options for the PDF path, output path and the voice model name; build the engine in the composition root only; map errors to exit codes; expose `python -m pdf_to_audiobook` and a console script in `pyproject.toml`. | No | BC-001 objective 1 |
| 4 | Write the end-to-end and CLI tests | Test the converter with the test double, the CLI with `main(argv)`, and the error exits; check coverage of at least 90 %. | No | Success criterion 3 |
| 5 | Scan and capture screenshots for steps 4 and 5 | Run the opengrep scan, then render `step-04-cli.svg` (a real conversion of a short sample PDF with Coqui TTS) and `step-05-tests.svg` (the pytest run). | No | Success criteria 4 and 6 |

---

[BC-001]: ../business-case.md
[RC-007]: ../sqa/reviews/rc-007-mil-004-converter-and-cli.md
