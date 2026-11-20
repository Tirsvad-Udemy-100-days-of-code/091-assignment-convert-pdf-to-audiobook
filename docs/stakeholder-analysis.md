# Stakeholder Analysis

## Metadata
| Key | Value |
| --- | --- |
| ID | SA-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Deprecated | Jens Tirsvad Nielsen | S01 | Initial version | [77d0001] |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-002]; stand-in for S01, not independent; language criteria confirmed by S01 in chat | [77d0001] |

---

## Purpose

The analysis names the people affected by the PDF to Audiobook project, how much power and interest each has, and what each expects, so that the Business Case, the plan and the reviews can cite stable IDs. It uses the power/interest grid and maps concerns to FURPS+.

## Stakeholder Summary Table

| ID | Name | Role/Title | Organization | Power Level | Interest Level | Quadrant | Primary Concern (Business Language) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Jens Tirsvad Nielsen | Course participant, Product Owner, developer and reviewer | Personal project | HIGH | HIGH | Manage Closely | Finish the assignment, learn from it, and keep every step planned and reviewed |
| S02 | Udemy coursists | Fellow participants of the Python bootcamp | Udemy | LOW | HIGH | Keep Informed | Readable, runnable code with the assignment's function names, and README instructions to run it |
| S03 | GitHub viewers | Browsers of the public repository | GitHub community | LOW | LOW | Monitor | A clear repository description, topics and README, and no runtime dependencies |

## Power/Interest Classification Rationale

- **Manage Closely (S01):** decides scope, reviews and accepts every artifact, and does the work.
- **Keep Informed (S02):** cannot change the project, but their use of the code is the purpose of sharing it; the README and wiki are written for them.
- **Monitor (S03):** casual visitors; a good description and topics are enough to serve them.

## Primary Concerns and FURPS+ Mapping

| Concern ID | Stakeholder | Concern | FURPS+ attribute |
| --- | --- | --- | --- |
| CN-001 | S01 | The program converts a PDF to speech and every step is traceable to a reviewed plan | Functionality |
| CN-002 | S01 | Tests run offline and fast because no paid or hosted service is used | Reliability |
| CN-003 | S02 | Code is easy to read and uses the assignment's function names | Usability |
| CN-004 | S02 | Instructions to create a `.venv` and to run the program and tests work as written | Usability |
| CN-005 | S03 | The repository has a clear description, topics and README | Usability |
| CN-006 | S03 | Installing the project pulls in no runtime dependencies | Supportability |

## Communication Requirements

| ID | Channel | Frequency | Deliverable | Phase / Milestone |
| --- | --- | --- | --- | --- |
| COM-001 | Chat with S01 | At plan acceptance and at the end of the run | Dry-run plan; run summary with every review verdict | All |
| COM-002 | Pull request per milestone | Once per milestone | Reviewed change with closing issue lines | MIL-001 to MIL-005 |
| COM-003 | README and wiki (en, da, ms) | Once, at the end | Instructions, lecture steps, screenshots | MIL-005 |
| COM-004 | Repository description and topics | Once | Short description and topics on the git host | MIL-001 |

## Conflicting Interests and Mitigations

| Conflict | Stakeholders | Mitigation |
| --- | --- | --- |
| S03 wants no runtime dependencies, but reading a PDF and speaking need libraries | S03, S01 | ADR-0001: two required dependencies, `pypdf` (pure Python) and Coqui TTS; nothing else at runtime; the README states the size of the install |
| S02 wants a good voice, but the project pays for no service | S02, S01 | Coqui TTS gives a natural voice for free on the user's machine; the cost is a larger install and a first-run model download, explained in the README |

## Traceability Analysis

### Business Goal Alignment

| Stakeholder | Concern | Business Case objective |
| --- | --- | --- |
| S01 | CN-001 | [BC-001] objectives 1, 2 and 3 |
| S01 | CN-002 | [BC-001] objective 4 |
| S02 | CN-003, CN-004 | [BC-001] objective 5 |
| S03 | CN-005 | [BC-001] objective 5 |
| S03 | CN-006 | [BC-001] objective 3 and success criterion 7 |

## Sign-Off

| Stakeholder | Decision | Date |
| --- | --- | --- |
| S01 | Pending review | |

---

[BC-001]: ./business-case.md
[RC-002]: ./sqa/reviews/rc-002-stakeholder-analysis.md
[77d0001]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/77d0001724a50e0bcd2472de88d61f866cf9ece0
