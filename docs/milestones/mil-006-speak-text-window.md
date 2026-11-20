# Speak Text Window

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-006 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Proposed | Jens Tirsvad Nielsen | S01 | Initial version | pending |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-015]; stand-in for S01, not independent; plan accepted by S01 in chat | pending |

---

## Purpose

Decide whether the user can type text into a small desktop window and hear it through the speakers, using the same Coqui TTS engine as the converter.

## Deliverable

A speak-text use case, an audio player port with a `sounddevice` adapter, a Tkinter window (MVVM, with a testable view model), the console script `pdf-to-audiobook-window`, ADR-0002 for the new runtime dependency, tests, and the README and wiki step 6 in en, da and ms.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `speak_text(text, engine, player)` splits the text into chunks, synthesizes each chunk and passes each clip to the player; a test with the engine and player doubles shows the clips arrive in order, and empty text is rejected with a readable error | Met | Not met |
| 2 | The audio player is a port in the domain layer; the `sounddevice` adapter is in the infrastructure layer and is imported lazily, so the package imports without `sounddevice` | Met | Not met |
| 3 | The window view model holds the text, the status and the busy flag; tests with the doubles show that Speak is disabled while speaking and that an error is shown as a message, not a traceback | Met | Not met |
| 4 | The window runs in a Docker container under `xvfb` (see `framework/process/gui-testing.md`), starts, accepts text, and writes a log and a screenshot to a shared folder; nothing is started on the host desktop | Met | Not met |
| 5 | A real run on the maintainer's machine with Coqui TTS and `sounddevice` plays a short sentence and the run is logged (exit code, device name, duration); the sound is not heard by the AI | Met | Not met |
| 6 | ADR-0002 records the `sounddevice` decision and is reviewed Go; `pyproject.toml` pins it with `~=` | Met | Not met |
| 7 | `pytest --cov` reports at least 90 % of the lines of `src/` and the opengrep scan reports 0 error findings | Met | Not met |
| 8 | `docs/images/step-06-window.svg` exists, and the README and the wiki in en, da and ms describe step 6 | Met | Not met |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-003 | The window uses the Coqui TTS engine |
| MIL-004 | The window reuses the text chunking and the composition root pattern |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| BC-001 objective 1 (speech from text) | Success criteria 1, 2, 5 |

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
| 1 | Write ADR-0002 for sounddevice | Record why `sounddevice` is the playback package, the PortAudio requirement, and the alternatives (`winsound`, no playback). Add the pinned dependency to `pyproject.toml`. | No | BC-001 objective 1 |
| 2 | Implement the speak_text use case and the player port | Add `AudioPlayer` in the domain layer and `speak_text(text, engine, player)` in the application layer; reuse `split_text_into_chunks`; reject empty text. | No | BC-001 objective 1 |
| 3 | Implement the sounddevice adapter | Add `SoundDevicePlayer` in the infrastructure layer: read a WAV clip with `wave`, play it and wait; import `sounddevice` lazily; map a missing device to a readable error. | No | BC-001 objective 1 |
| 4 | Implement the Tkinter window | Add a view model (text, status, busy) and a Tkinter view with a text box and a Speak button; speak on a worker thread so the window stays responsive; build the engine and player in the composition root; add the console script `pdf-to-audiobook-window`. | No | BC-001 objective 1 |
| 5 | Write the unit and view model tests | Test `speak_text`, the player adapter with a fake `sounddevice` module, and the view model with the doubles; coverage of at least 90 %. | No | Success criteria 1, 2, 3, 7 |
| 6 | Run the window test in a Docker container | Run the window under `xvfb` in a Linux container, with a log and a screenshot in a shared folder, per `gui-testing.md`. If Docker is not available, stop and report; do not use the host desktop. | No | Success criterion 4 |
| 7 | Make the real playback run | Run the real window path on the maintainer's machine with a short sentence and log the result; this is the only step that uses the speakers. | No | Success criterion 5 |
| 8 | Scan, screenshot and document step 6 | Run the opengrep scan, render `step-06-window.svg` from the container screenshot or log, update the README, and add wiki page Step-6 in en, da and ms with the sidebar and the Home link. | No | Success criteria 7 and 8 |

---

[BC-001]: ../business-case.md
[RC-015]: ../sqa/reviews/rc-015-mil-006-speak-text-window.md
