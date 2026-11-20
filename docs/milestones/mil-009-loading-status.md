# Loading Status

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-009 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | Jens Tirsvad Nielsen | S01 | Initial version | pending |
| 2026-11-21 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-022]; stand-in for S01, not independent; plan accepted by S01 in chat | pending |

---

## Purpose

Decide whether the window tells the user that the voice model is loading, so the first sound, which takes several seconds, no longer looks like a frozen window.

## Deliverable

A load notification from the Coqui TTS adapter, a "Loading voice" status in the window and a "Speaking" status after it, tests, and a short note in the README and the wiki (step 6 in en, da and ms).

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | The Coqui TTS adapter calls an optional `on_loading` callback once, before the model loads, and never when the model is already loaded; a test with a fake loader shows one call for two `synthesize` calls | Met | Not met |
| 2 | The view model shows `Loading voice...` while the model loads, then `Speaking...`, then `Done`; a test with the doubles records this order | Met | Not met |
| 3 | A model that fails to load still ends in `error: ...`, and the busy flag is cleared | Met | Not met |
| 4 | The domain and application layers do not change; the callback is wired in the composition root of the window only | Met | Not met |
| 5 | The window test in the Linux container on a virtual display shows the status text in its log and the screenshot, and nothing is started on the host desktop | Met | Not met |
| 6 | `pytest --cov` reports at least 90 % of the lines of `src/` and the opengrep scan, including the host scan, reports 0 error findings | Met | Not met |
| 7 | The README and the wiki step 6 page in en, da and ms mention the loading status | Met | Not met |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-006 | The window and its view model |
| MIL-008 | The adapter changes of the quiet console |

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
| 1 | Add the load notification | Give `CoquiSpeechEngine` an optional `on_loading` callback that is called once, just before the model loads; the speech port does not change. | No | BC-001 objective 1 |
| 2 | Show the loading status | Wire the callback to the view model in the window composition root; the status goes `Loading voice...`, `Speaking...`, `Done` or `error: ...`; the view updates on the main thread. | No | BC-001 objective 1 |
| 3 | Write the tests | Test one call per load, the status order, the load failure and the thread-safe update; coverage of at least 90 %. | No | Success criteria 1 to 4, 6 |
| 4 | Run the window test in the Docker container | Extend the container test so that its log records the status sequence; take a screenshot, per `gui-testing.md`. | No | Success criterion 5 |
| 5 | Scan and document | Run the opengrep scan and update the README and the wiki step 6 in en, da and ms. | No | Success criteria 6 and 7 |

---

[BC-001]: ../business-case.md
[RC-022]: ../sqa/reviews/rc-022-mil-009-loading-status.md
