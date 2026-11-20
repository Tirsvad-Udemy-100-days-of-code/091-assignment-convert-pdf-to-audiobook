# PDF Text Extraction

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-002 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Deprecated | Jens Tirsvad Nielsen | S01 | Initial version | [77d0001] |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-005]; stand-in for S01, not independent; language criteria confirmed by S01 in chat | [77d0001] |

---

## Purpose

Decide whether text can be read from a PDF and split into pieces the speech services accept.

## Deliverable

`extract_text_from_pdf` and `split_text_into_chunks` in the package, with a generated sample PDF used by the tests, and the screenshot of lecture step 2.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `pytest` passes with at least 90 % line coverage of the new modules | Met | Not met |
| 2 | A generated one-page and a multi-page PDF yield the expected text in page order | Met | Not met |
| 3 | A PDF with no text raises the package error `PdfTextError` with a readable message | Met | Not met |
| 4 | No chunk is longer than `MAX_CHUNK_CHARS` and no word is cut in half | Met | Not met |
| 5 | The opengrep scan of the branch reports 0 error findings | Met | Not met |
| 6 | `docs/images/step-02-extract-text.svg` exists | Met | Not met |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-001 | Skeleton, tooling and scan procedure |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| BC-001 objective 2 | Success criteria 1, 2, 3 |

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
| 1 | Write the PDF test fixture builder | Add a helper in `tests/` that writes minimal valid PDFs with known text using only the standard library, so tests need no binary files and no network. | No | Success criterion 2 |
| 2 | Implement extract_text_from_pdf | Read a PDF path with `pypdf` and return the text of all pages in order; raise `PdfTextError` for a missing file, an unreadable file, or a PDF with no extractable text. Document it with Doxygen comments. | No | BC-001 objective 2 |
| 3 | Implement split_text_into_chunks | Split text on sentence and paragraph boundaries into chunks no longer than `MAX_CHUNK_CHARS` (in `constants.py`), never cutting a word; a single word longer than the limit is split as a last resort. | No | BC-001 objective 2 |
| 4 | Test extraction and chunking | Write pytest tests for the cases in the Go criteria, including empty text, one very long sentence and non-ASCII text. | No | Success criterion 3 |
| 5 | Scan and capture the step 2 screenshot | Run the opengrep scan, then render `step-02-extract-text.svg` from a real run of extraction on the sample PDF. | No | Success criteria 4 and 6 |

---

[BC-001]: ../business-case.md
[RC-005]: ../sqa/reviews/rc-005-mil-002-pdf-text-extraction.md
[77d0001]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/77d0001724a50e0bcd2472de88d61f866cf9ece0
