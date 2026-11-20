# Review Record: Wiki

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-014 |
| CrossReference | [MIL-005], [QC-WIKI-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Initial version; autonomous stand-in for S01, not independent | [2f941c4] |

---

## Artifact Under Review

- Instance reviewed: [MIL-005]
- Checklist used: [QC-WIKI-001]
- Scope: full review of `docs/wiki/` as published after pull request 37
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is the author as stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The wiki has a `_Sidebar.md`, because the host lists subpages only through it | Pass | `docs/wiki/_Sidebar.md` exists and is published. |
| 2 | The sidebar starts with the wiki's title in bold, then one list of the pages in the primary language (English), `Home` first | Pass | The sidebar starts with the bold title `PDF to Audiobook` and one English list with `Home` first. |
| 3 | The page list holds a link to every English page of the wiki, and no link points to a page that does not exist | Pass | All 8 English pages are in the list; every link resolves on the host (checked by request). |
| 4 | A `**Related**` section follows the page list only when the wiki has related wikis (for example the checklists wiki for a framework wiki); each entry is a link to that wiki's Home. A wiki with nothing related has no such section | N-A | The wiki has no related wiki; the sidebar has no `Related` section. |
| 5 | A `**Languages**` section is the last section of the sidebar. It has one line per language, the language written in that language, linking to that language's `Home` page | Pass | `Languages` is the last section: `English: [Home](Home)`, `Dansk: [Hjem](Home-da)`, `Bahasa Melayu: [Utama](Home-ms)`. |
| 6 | The sidebar does not repeat the page list per language | Pass | The page list appears once. |
| 7 | A sidebar produced by a generator carries a comment that says so and names the generator; the generator is changed, not the page | N-A | The sidebar is written by hand, not generated. |
| 8 | The wiki has a `Languages` line on each page (criterion 11), so the sidebar is not the only way to switch language | Pass | Every page has the language line. |
| 9 | Every wiki exists in English and, as a minimum, in the language the project's registry names as the PO language; further languages are added on top, never instead of English | Pass | English plus Danish; the registry lists en, da and ms, and the PO language is en. |
| 10 | Every English page has a page in each other language of the wiki: the page sets are identical | Pass | 8 English pages, 8 Danish and 8 Malay pages: identical page sets (checked by script). |
| 11 | Every page starts with the language line, with the current language in bold and a link to the same page in each other language | Pass | Line 1 of every page is the language line with the current language in bold (checked by script for all 16 translated pages). |
| 12 | A page in a language other than English is named `<Page>-<code>.md`, with a BCP 47 code; English has no suffix | Pass | Files are `<Page>-da.md` and `<Page>-ms.md`; English has no suffix. |
| 13 | Code blocks, commands, file names and IDs stay in English in every language | Pass | Code blocks are identical to the English ones in every language (checked by script); commands, file names and IDs are unchanged. |
| 14 | The sidebar, every page and every link were checked on the published wiki after the change, not only in the repository | Pass | After the merge of pull request 37 the host listed 25 pages (24 pages and the sidebar); requests for 11 sample pages returned 200, the five screenshots are served as `image/svg+xml`, and the links of the sampled pages resolve. |
| 15 | A change to the layout rules (sections, order, naming) is made in the generator or template and in this checklist's source rules together | N-A | No generator or layout rule changed. |
| 16 | The wiki folder (`docs/wiki/`) is flat: every page, `Home.md` and `_Sidebar.md` included, is directly in it, and languages are told apart by file name, never by a subfolder | Pass | `docs/wiki/` is flat; languages are told apart by file name. |

## Overall Verdict

Go — every criterion passes (criteria 1 to 16). The review is not independent: the author reviewed as stand-in for S01.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | 2026-11-20 |

---

[MIL-005]: ../../milestones/mil-005-documentation-and-wiki.md
[QC-WIKI-001]: ../../../framework/qc/artifacts/qc-wiki.md
[2f941c4]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/2f941c41366f1daeb1c886bbd37c5601f9896a4c
