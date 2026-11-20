# Open PDF in the Window

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-007 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Proposed | Jens Tirsvad Nielsen | S01 | Initial version | [ee19880] |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-018]; stand-in for S01, not independent; plan accepted by S01 in chat | [ee19880] |

---

## Purpose

Decide whether the user can open a PDF file from the window and hear its text through the speakers, so the window covers the assignment's PDF to speech goal.

## Deliverable

An Open PDF button and a file dialog in the window, a `speak_pdf` use case that reads the PDF text and speaks it, a Stop control, tests, and the README and wiki step 7 in en, da and ms.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `speak_pdf(pdf_path, engine, player, extract_text)` reads the text with the injected extractor and speaks every chunk in page order; a test with the doubles and a generated PDF shows the clips arrive in order | Met | Not met |
| 2 | A missing, unreadable or empty PDF gives a readable message in the window status, not a traceback | Met | Not met |
| 3 | The view model has an `open_pdf(path)` command and a Stop command; tests with the doubles show that Stop ends the speech between two chunks and that Speak, Open and Stop are enabled only when they make sense | Met | Not met |
| 4 | The file dialog is behind a small port, so tests choose a file without a dialog | Met | Not met |
| 5 | The window test in the Linux container on a virtual display opens the sample PDF, reaches the status Done and writes a log and a screenshot; nothing is started on the host desktop | Met | Not met |
| 6 | One real playback run on the maintainer's machine speaks the sample PDF through the speakers and is logged (exit code, device name, duration) | Met | Not met |
| 7 | `pytest --cov` reports at least 90 % of the lines of `src/` and the opengrep scan, including the host scan, reports 0 error findings | Met | Not met |
| 8 | `docs/images/step-07-open-pdf.svg` exists, and the README and the wiki in en, da and ms describe step 7 | Met | Not met |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-006 | The window, the player and `speak_text` |
| MIL-002 | The PDF text extractor |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| BC-001 objective 1 (PDF to speech) | Success criteria 1, 2, 5 |

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
| 1 | Implement the speak_pdf use case | Add `speak_pdf(pdf_path, engine, player, extract_text, should_stop)` in the application layer: extract the text, reject an empty PDF, speak chunk by chunk through the player and stop between chunks when asked. | No | BC-001 objective 1 |
| 2 | Add the file chooser port and the dialog adapter | Add a `FileChooser` port; the Tkinter adapter uses `filedialog.askopenfilename` limited to PDF files; tests use a fake chooser. | No | BC-001 objective 1 |
| 3 | Extend the view model and the window | Add `open_pdf(path)` and Stop to the view model and an Open PDF button and a Stop button to the view; show the file name and a readable error in the status. | No | BC-001 objective 1 |
| 4 | Write the tests | Test `speak_pdf` with a generated PDF, the empty and missing PDF cases, Stop, and the view model; coverage of at least 90 %. | No | Success criteria 1, 2, 3, 4, 7 |
| 5 | Run the window test in the Docker container | Extend the container test to open `tests/data/sample.pdf` through the fake chooser and reach Done, with a log and a screenshot, per `gui-testing.md`. | No | Success criterion 5 |
| 6 | Make the real playback run | Speak the sample PDF through the real engine and speakers without opening a window on the host desktop; log the result. | No | Success criterion 6 |
| 7 | Scan, screenshot and document step 7 | Run the opengrep scan, render `step-07-open-pdf.svg` from the container screenshot, update the README, and add wiki page Step-7 in en, da and ms with the sidebar and the Home link. | No | Success criteria 7 and 8 |

---

[BC-001]: ../business-case.md
[RC-018]: ../sqa/reviews/rc-018-mil-007-open-pdf-in-window.md
[ee19880]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/ee198802ba382293f2aae14950aa65ff5ba82dea
