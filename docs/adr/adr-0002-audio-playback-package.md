# ADR-0002: Audio playback package

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0002 |
| CrossReference | [BC-001], [ADR-0001], [MIL-006] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-20 | Accepted | Jens Tirsvad Nielsen | S01 | Initial version; reviewed Go in [RC-016]; stand-in for S01, not independent | [359c357] |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The speak-text window of [MIL-006] must play the synthesized speech through the speakers. The standard library has no cross-platform audio output. Options:

1. `winsound` from the standard library: no new package, but it exists only on Windows and the project runs on Windows, macOS and Linux.
2. Write the sound to a file and open it with the operating system's player: no package, but it starts a second program, cannot wait for the end of the sound and is hard to test.
3. `sounddevice`: a small package that plays an array of samples through PortAudio on Windows, macOS and Linux, and can wait until the sound ends.

## Decision

`sounddevice` is the playback package, behind an `AudioPlayer` port in the domain layer, so the speaking logic does not import it. It is declared in `pyproject.toml` as `sounddevice~=0.5` and is imported only when a sound is played.

## Consequences

**Positive:**

- One code path on Windows, macOS and Linux.
- Playback blocks until the sound ends, so chunks are spoken in order without gaps or overlaps.
- The port lets tests replace the speakers with a test double; no test makes a sound.

**Negative:**

- One more runtime dependency, on top of the two of [ADR-0001]. It brings `numpy` and `cffi`; the PyTorch install already brings `numpy`.
- On Linux the PortAudio library must be installed by the system (`libportaudio2`); the Windows and macOS wheels bundle it.
- With no output device the player fails; the window shows a readable message instead of a traceback.

## Affected Artifacts

- [BC-001] — success criterion 7 on the number of required packages (already noted as an open inconsistency in the traceability matrix)
- [ADR-0001] — the list of runtime packages grows by one
- [MIL-006] — the milestone that needs playback

[BC-001]: ../business-case.md
[ADR-0001]: ./adr-0001-runtime-dependencies.md
[MIL-006]: ../milestones/mil-006-speak-text-window.md
[RC-016]: ../sqa/reviews/rc-016-adr-0002-audio-playback-package.md
[359c357]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/commit/359c357f97c4df7626b2f192adeb4e44062597c4
