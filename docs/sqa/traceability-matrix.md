# Traceability Matrix

## Metadata
| Key | Value |
| --- | --- |
| ID | TM-001 |
| CrossReference | [BC-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Deprecated | Jens Tirsvad Nielsen | S01 | Accepted by S01 as Product Owner through plan acceptance in chat; no checklist exists for the Traceability Matrix | [77d0001] |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Restored the Purpose, Traceability Table, Concern Coverage and Open Inconsistencies sections that the previous row lost, and added the review records of the code and the wiki; accepted by S01 as Product Owner, no checklist exists | pending |

---

## Purpose

Tracks backward/forward links between artifact instances so that the Business Case's
cross-artifact traceability success criterion is measurable. A row is added or
updated whenever an artifact instance is created or reviewed.

## Traceability Table

| Artifact Instance | Type | Language | Domain | Upstream (Backward Link) | Downstream (Forward Link) | Last Reviewed (RC-ID) |
| --- | --- | --- | --- | --- | --- | --- |
| [BC-001] | Business Case | en | it | - | [SA-001] | [RC-001] |
| [SA-001] | Stakeholder Analysis | en | it | [BC-001] | [PP-001] | [RC-002] |
| [PP-001] | Project Plan | en | it | [BC-001], [SA-001] | [MIL-001], [MIL-002], [MIL-003], [MIL-004], [MIL-005] | none (no checklist) |
| [ADR-0001] | Architecture Decision Record | - | - | [BC-001], [SA-001] | [MIL-003] | [RC-011] |
| [MIL-001] | Milestone | en | it | [BC-001], [PP-001] | code of MIL-001 | [RC-004], [RC-009] |
| [MIL-002] | Milestone | en | it | [BC-001], [PP-001] | code of MIL-002 | [RC-005], [RC-010] |
| [MIL-003] | Milestone | en | it | [BC-001], [PP-001], [ADR-0001] | code of MIL-003 | [RC-006], [RC-012] |
| [MIL-004] | Milestone | en | it | [BC-001], [PP-001] | code of MIL-004 | [RC-007], [RC-013] |
| [MIL-005] | Milestone | en | it | [BC-001], [PP-001] | README and wiki | [RC-008], [RC-014] |

## Concern Coverage

| Concern (CN-ID) | Views that answer it | Decisions (ADR) | Quality check (TP) | Status |
| --- | --- | --- | --- | --- |
| CN-001 | [BC-001], [MIL-004] | - | - | Covered |
| CN-002 | [MIL-003] | [ADR-0001] | - | Covered |
| CN-003 | [MIL-004], [MIL-005] | - | - | Covered |
| CN-004 | [MIL-001], [MIL-005] | - | - | Covered |
| CN-005 | [MIL-001], [MIL-005] | - | - | Covered |
| CN-006 | [BC-001] | [ADR-0001] | - | Gap: two required packages remain, see the conflict in [SA-001] |

## Open Inconsistencies

| # | Views | Inconsistency | Found in (RC-ID) | Status | Resolution |
| --- | --- | --- | --- | --- | --- |
| 1 | [BC-001], [ADR-0001] | Success criterion 7 says "2 required packages" while `pyproject.toml` declares four requirement lines (Coqui TTS needs PyTorch, which it does not declare); the ADR explains it | [RC-011] | Open | Accepted as is; reword in the next Business Case revision |

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
[ADR-0001]: ../adr/adr-0001-runtime-dependencies.md
[MIL-001]: ../milestones/mil-001-project-foundation.md
[MIL-002]: ../milestones/mil-002-pdf-text-extraction.md
[MIL-003]: ../milestones/mil-003-speech-engines.md
[MIL-004]: ../milestones/mil-004-converter-and-cli.md
[MIL-005]: ../milestones/mil-005-documentation-and-wiki.md
[RC-001]: ./reviews/rc-001-business-case.md
[RC-002]: ./reviews/rc-002-stakeholder-analysis.md
[RC-003]: ./reviews/rc-003-adr-0001-runtime-dependencies.md
[RC-004]: ./reviews/rc-004-mil-001-project-foundation.md
[RC-005]: ./reviews/rc-005-mil-002-pdf-text-extraction.md
[RC-006]: ./reviews/rc-006-mil-003-speech-engines.md
[RC-007]: ./reviews/rc-007-mil-004-converter-and-cli.md
[RC-008]: ./reviews/rc-008-mil-005-documentation-and-wiki.md
[77d0001]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/77d0001724a50e0bcd2472de88d61f866cf9ece0
[RC-009]: ./reviews/rc-009-mil-001-code.md
[RC-010]: ./reviews/rc-010-mil-002-code.md
[RC-012]: ./reviews/rc-012-mil-003-code.md
[RC-013]: ./reviews/rc-013-mil-004-code.md
[RC-011]: ./reviews/rc-011-adr-0001-delta.md
[RC-014]: ./reviews/rc-014-wiki.md
