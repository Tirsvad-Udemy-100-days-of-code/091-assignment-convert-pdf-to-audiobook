# ADR-0001: Runtime dependencies

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0001 |
| CrossReference | [BC-001], [SA-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Deprecated | Jens Tirsvad Nielsen | S01 | Initial version | [77d0001] |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-003]; stand-in for S01, not independent | [77d0001] |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The Business Case asks for few runtime dependencies (success criterion 7), and S03 wants none. The program still needs two things the standard library does not give:

1. Reading text from a PDF. Options: write a parser on `zlib` (fragile, wrong on many PDFs), or depend on `pypdf`, a pure Python library with no further dependencies.
2. A voice. Paid web services (iSpeech, Google Cloud TTS, Amazon Polly) were considered and rejected by the Product Owner because the project does not pay. `pyttsx3` was considered and dropped. Coqui TTS is free, runs locally and gives a natural neural voice, but it is a large install (a machine learning runtime) and downloads a voice model on first use; its support for Python 3.13 must be checked in MIL-003.

## Decision

`pypdf` and Coqui TTS are the two required runtime dependencies, both declared in `pyproject.toml`. Coqui TTS is the only speech engine and sits behind a `SpeechEngine` port. There is no HTTP client, no API key and no fallback engine. Test tools (`pytest`, `pytest-cov`) are in a `dev` extra. If Coqui TTS does not install on Python 3.13, the run stops and reports.

## Consequences

**Positive:**

- No paid account, no secret and no network call in the program itself.
- A natural voice that works offline after the first model download.
- Default tests run fast because they use a test double of the engine.

**Negative:**

- S03's wish for "no runtime dependencies" is not met: two remain, and one is large. The conflict is recorded in the Stakeholder Analysis.
- The first install and the first run download several hundred megabytes; the README says so.
- With one engine there is no fallback: if Coqui TTS fails, the conversion fails with a clear message.

## Affected Artifacts

- [BC-001] — success criterion 7 reads "at most 1 required dependency"
- [SA-001] — conflict between S03's concern and the need to read PDFs
[RC-003]: ../sqa/reviews/rc-003-adr-0001-runtime-dependencies.md
[77d0001]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/77d0001724a50e0bcd2472de88d61f866cf9ece0
