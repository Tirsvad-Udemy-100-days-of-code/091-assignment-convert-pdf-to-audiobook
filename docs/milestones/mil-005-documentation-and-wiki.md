# Documentation and Wiki

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-005 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Deprecated | Jens Tirsvad Nielsen | S01 | Initial version | pending |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Reviewed Go in [RC-008]; stand-in for S01, not independent; language criteria confirmed by S01 in chat | pending |

---

## Purpose

Decide whether the project can be handed to course participants and repository viewers.

## Deliverable

The final README from the framework template with the five screenshots, generated Doxygen documentation, and a wiki in English, Danish and Bahasa Malaysia that explains what each lecture step taught, including a reflection page.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `bash framework/scripts/check-readme.sh` exits 0 and the README shows the five screenshots | Met | Not met |
| 2 | README explains the `.venv` creation, `python -m pip install --upgrade pip`, running the program and running the tests, and a reader following only it succeeds in a clean clone | Met | Not met |
| 3 | `doxygen Doxyfile` runs with no warnings about undocumented public functions | Met | Not met |
| 4 | `docs/wiki/` has the same pages in `<Page>.md`, `<Page>-da.md` and `<Page>-ms.md`, a `_Sidebar.md` with the Languages section, and passes `QC-WIKI-001` | Met | Not met |
| 5 | Every lecture step page has its screenshot and a section on what was gained | Met | Not met |
| 6 | The wiki is enabled on the git host and the published pages are read back | Met | Not met |
| 7 | The opengrep scan of the branch reports 0 error findings; the words for artificial intelligence do not occur in any artifact | Met | Not met |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-004 | Documentation describes the finished program |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| BC-001 objective 5 | Success criteria 5 and 6 |

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
| 1 | Write the final README | Fill the framework README template: overview, requirements, setup with `.venv`, run, tests, license, links, appendix; embed the five screenshots; check with `check-readme.sh`. | No | CN-003, CN-004 |
| 2 | Run Doxygen and fix documentation gaps | Run `doxygen Doxyfile`, add missing comments, and keep the output out of git. | No | BC-001 scope |
| 3 | Write the English wiki | Write Home, Setup, one page per lecture step (five), Design, Testing, Reflection and the sidebar; each step page embeds its screenshot and says what was gained. | No | Success criteria 5 and 6 |
| 4 | Translate the wiki to Danish and Bahasa Malaysia | Write every page again as `<Page>-da.md` and `<Page>-ms.md` with the language line; commands, code and file names stay in English. | No | Wiki rule 2 |
| 5 | Publish and verify the wiki | Check the wiki is enabled, the `docs/wiki/` folder is merged to main, and the published pages and sidebar links work; review against `QC-WIKI-001`. | No | Success criterion 5 |
| 6 | Write the reflection | Record how the project was approached, what was hard and easy, the biggest lesson and what to do differently next time, in the Reflection wiki page in three languages. | No | Assignment reflection |
| 7 | Final scan and release check | Run the opengrep scan, the full test run and the framework checks; search all artifacts for the forbidden word; summarise the run for S01. | No | Success criteria 4 and 5 |

---

[BC-001]: ../business-case.md
[RC-008]: ../sqa/reviews/rc-008-mil-005-documentation-and-wiki.md
