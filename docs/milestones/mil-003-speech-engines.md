# Speech Engines

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-003 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Deprecated | Jens Tirsvad Nielsen | S01 | Initial version | [77d0001] |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-006]; stand-in for S01, not independent; language criteria confirmed by S01 in chat | [77d0001] |

---

## Purpose

Decide whether text can be turned into speech by Coqui TTS on this machine, behind a port, with tests that need neither network nor model.

## Deliverable

A `SpeechEngine` port, a Coqui TTS engine that writes WAV audio, a test double used by the default tests, one optional slow test of the real engine, and the screenshot of lecture step 3.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Coqui TTS installs in a fresh `.venv` on Python 3.13 and a one-sentence synthesis writes a WAV file (checked first; a failure stops the run) | Met | Not met |
| 2 | The default `pytest` run passes with sockets blocked and without the Coqui TTS model | Met | Not met |
| 3 | The domain layer does not import Coqui TTS; only the engine module does, and it imports it lazily | Met | Not met |
| 4 | A text longer than `MAX_CHUNK_CHARS`, an empty text and a missing model each give a clear package error | Met | Not met |
| 5 | The slow test, marked `slow` and skipped by default, synthesizes real audio and passes when run | Met | Not met |
| 6 | `pytest` passes with at least 90 % line coverage of the new modules and the opengrep scan reports 0 error findings | Met | Not met |
| 7 | `docs/images/step-03-coqui-tts.svg` exists | Met | Not met |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-002 | Chunks are the input of the engines |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| BC-001 objective 3 | Success criteria 1, 2, 4, 7 |

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
| 1 | Verify Coqui TTS installs on Python 3.13 | In a throw-away `.venv`, install the Coqui TTS package, download its default English voice model once and synthesize one sentence to a WAV file. Record the package name, version, model name and size in ADR-0001. If it does not work, stop the run and report, because the plan depends on it. | No | ADR-0001 |
| 2 | Define the SpeechEngine port and AudioClip | Add the abstract `SpeechEngine` with `synthesize(text)` returning an `AudioClip` (WAV bytes), and the errors `SpeechEngineError` and `EngineUnavailableError`, in the domain layer with no import of Coqui TTS. | No | BC-001 objective 3 |
| 3 | Implement the Coqui TTS engine | Import Coqui TTS lazily, load the model named in `constants.py` once, synthesize a chunk to a temporary WAV file, return it as an `AudioClip`, and map failures to the package errors. | No | BC-001 objective 3 |
| 4 | Write the test double and engine tests | Add `FakeSpeechEngine` in `tests/` that returns a short valid WAV, test the port contract and error mapping with a stubbed Coqui module, and add a socket-blocking fixture that proves the default tests make no request. | No | Success criterion 2 |
| 5 | Add the optional slow test | Add one test marked `slow` that synthesizes real audio with Coqui TTS, skipped unless `-m slow` is given; document it in the README later. | No | Success criterion 1 |
| 6 | Scan and capture the step 3 screenshot | Run the opengrep scan, then render `step-03-coqui-tts.svg` from a real synthesis of one sentence. | No | Success criteria 4 and 6 |

---

[BC-001]: ../business-case.md
[RC-006]: ../sqa/reviews/rc-006-mil-003-speech-engines.md
[77d0001]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/77d0001724a50e0bcd2472de88d61f866cf9ece0
