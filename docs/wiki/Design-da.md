[English](Design) · **Dansk** · [Bahasa Malaysia](Design-ms)

# Design

Koden ligger i fire lag under `src/pdf_to_audiobook/`. Et lag importerer kun lag længere inde.

| Lag | Indeholder | Må importere |
| --- | --- | --- |
| `domain` | `split_text_into_chunks`, `join_wav_clips`, `AudioClip`, porten `SpeechEngine`, fejlene | standardbiblioteket |
| `application` | `convert_pdf_to_audiobook` | `domain` |
| `infrastructure` | `extract_text_from_pdf` (pypdf), `CoquiSpeechEngine` (Coqui TTS) | `domain` |
| `presentation` | kommandolinjen og kompositionsroden | alt |

Alle konstanter ligger i `constants.py`. Kommentarer bruger Doxygen-stilen (`!@brief`, `@param`, `@return`, `@throws`).

## Afhængigheder

To påkrævede pakker: `pypdf` og Coqui TTS. Coqui TTS installeres med sine ekstrapakker `codec` og `languages` og med PyTorch, som den har brug for, men ikke angiver. Beslutningen står i ADR-0001 i `docs/adr/`.

## Proces

Projektet følger en proces, hvor planlægningen kommer først: Business Case, interessentanalyse, projektplan, fem milepæle og så kode. Hver milepæl var én gren og én pull request, gennemgået før den blev flettet. Dokumenterne ligger i mappen `docs/` i repositoriet.
