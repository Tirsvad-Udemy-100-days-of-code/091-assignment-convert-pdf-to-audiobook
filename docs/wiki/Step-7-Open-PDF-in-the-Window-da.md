[English](Step-7-Open-PDF-in-the-Window) · **Dansk** · [Bahasa Malaysia](Step-7-Open-PDF-in-the-Window-ms)

# Trin 7: Åbn en PDF i vinduet

![Trin 7: åbn en PDF og hør den](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-07-open-pdf.svg)

## Hvad vi gjorde

- Vi tilføjede en Open PDF-knap og en Stop-knap til vinduet. Open PDF viser en fildialog for PDF-filer, læser teksten med `pypdf` og læser den op side for side i højttalerne.
- `speak_pdf(pdf_path, engine, player, extract_text)` er anvendelsesfaldet. Tekstudtrækkeren og filvælgeren injiceres, så anvendelsesfaldet aldrig importerer `pypdf` eller Tkinter, og tests vælger en fil uden dialog.
- `speak_text` og `speak_pdf` deler én løkke, `speak_chunks`, så reglen "tjek for Stop, læs en bid op, afspil den" findes ét sted. Stop afbryder oplæsningen mellem to bidder.
- En manglende, ulæselig eller tom PDF vises som en besked i statuslinjen, ikke som en traceback.

```powershell
pdf-to-audiobook-window
pwsh scripts/gui-test.ps1
```

- Containertesten åbner `tests/data/sample.pdf` gennem en falsk filvælger på en virtuel skærm og når status Done (`pwsh scripts/gui-test.ps1`). Skærmbilledet ovenfor kommer derfra.
- Én rigtig kørsel læste eksempel-PDF'en op i højttalerne: 2 bidder, 23 sekunder, exitkode 0.

## Hvad vi fik ud af det

- Ved at injicere udtrækkeren og vælgeren kunne vinduet testes: kun den rigtige kørsel kræver en dialog og et lydkort.
- Én fælles løkke til indtastet tekst og PDF-tekst betød, at Stop virkede for begge med én ændring.
- `pypdf` importeres først når en PDF åbnes, så vinduet starter hurtigt, og containeren behøver den kun til denne test.
