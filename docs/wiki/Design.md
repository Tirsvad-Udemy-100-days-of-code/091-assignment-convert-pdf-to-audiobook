**English** · [Dansk](Design-da) · [Bahasa Malaysia](Design-ms)

# Design

The code is in four layers under `src/pdf_to_audiobook/`. A layer imports only layers inside it.

| Layer | Holds | May import |
| --- | --- | --- |
| `domain` | `split_text_into_chunks`, `join_wav_clips`, `AudioClip`, the `SpeechEngine` port, the errors | the standard library |
| `application` | `convert_pdf_to_audiobook` | `domain` |
| `infrastructure` | `extract_text_from_pdf` (pypdf), `CoquiSpeechEngine` (Coqui TTS) | `domain` |
| `presentation` | the command line and the composition root | everything |

All constants are in `constants.py`. Comments use the Doxygen style (`!@brief`, `@param`, `@return`, `@throws`).

## Dependencies

Two required packages: `pypdf` and Coqui TTS. Coqui TTS is installed with its `codec` and `languages` extras and with PyTorch, which it needs but does not declare. The decision is in ADR-0001 in `docs/adr/`.

## Process

The project follows a plan-first process: Business Case, Stakeholder Analysis, Project Plan, five milestones, then code. Each milestone was one branch and one pull request, reviewed before it merged. The documents are in the `docs/` folder of the repository.
