[English](Design) · [Dansk](Design-da) · **Bahasa Malaysia**

# Reka bentuk

Kod terbahagi kepada empat lapisan di bawah `src/pdf_to_audiobook/`. Sesuatu lapisan hanya mengimport lapisan di sebelah dalamnya.

| Lapisan | Mengandungi | Boleh mengimport |
| --- | --- | --- |
| `domain` | `split_text_into_chunks`, `join_wav_clips`, `AudioClip`, port `SpeechEngine`, ralat-ralat | pustaka standard |
| `application` | `convert_pdf_to_audiobook` | `domain` |
| `infrastructure` | `extract_text_from_pdf` (pypdf), `CoquiSpeechEngine` (Coqui TTS) | `domain` |
| `presentation` | baris perintah dan composition root | semua |

Semua pemalar berada dalam `constants.py`. Komen menggunakan gaya Doxygen (`!@brief`, `@param`, `@return`, `@throws`).

## Kebergantungan

Dua pakej wajib: `pypdf` dan Coqui TTS. Coqui TTS dipasang dengan extra `codec` dan `languages` serta PyTorch, yang diperlukannya tetapi tidak diisytiharkannya. Keputusan itu terdapat dalam ADR-0001 di `docs/adr/`.

## Proses

Projek ini mengikut proses perancangan dahulu: Business Case, Stakeholder Analysis, Project Plan, lima milestone, kemudian kod. Setiap milestone ialah satu branch dan satu pull request, disemak sebelum digabungkan. Dokumen-dokumen berada dalam folder `docs/` repositori.
