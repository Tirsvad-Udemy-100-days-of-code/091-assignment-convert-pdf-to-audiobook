[English](Step-2-Read-the-PDF) · **Dansk** · [Bahasa Malaysia](Step-2-Read-the-PDF-ms)

# Trin 2: Læs PDF'en

![Trin 2: læs PDF'en og del teksten op](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-02-extract-text.svg)

## Hvad vi gjorde

- `extract_text_from_pdf` læser hver side med `pypdf` og sætter sidernes tekster sammen.
- `split_text_into_chunks` skærer teksten ved afsnits- og sætningsslut i stykker på højst 400 tegn (`MAX_CHUNK_CHARS`), aldrig midt i et ord.
- En PDF uden tekst (for eksempel en scanning) giver en tydelig `PdfTextError` i stedet for stilhed.

```powershell
python tools/demo_extract.py tests/data/sample.pdf
```

## Hvad vi fik ud af det

- Talemotorer fungerer bedst med korte stykker tekst, så opdelingen er en egentlig forretningsregel, og den bor i domænelaget uden ind- eller udlæsning.
- Tests behøver ingen binære filer: en lille funktion fra standardbiblioteket bygger en gyldig PDF i farten.
- Fejl er navngivet efter det, der gik galt, og den oprindelige årsag bevares med `raise ... from`.
