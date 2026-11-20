[English](Step-5-Tests-and-Quality) · **Dansk** · [Bahasa Malaysia](Step-5-Tests-and-Quality-ms)

# Trin 5: Tests og kvalitet

![Trin 5: kør testene](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-05-tests.svg)

## Hvad vi gjorde

```powershell
python -m pytest
python -m pytest --cov=pdf_to_audiobook
python -m pytest -m slow
python -m ruff check src tests
python -m mypy
doxygen Doxyfile
pwsh scripts/scan.ps1
```

- 110 hurtige tests dækker 98 procent af kildekoden. En fixture blokerer netværket, så ingen test kan nå internettet.
- `ruff` tjekker stil, `mypy` i striks tilstand tjekker typer, og Doxygen bygger API-dokumentationen ud fra kommentarerne i kildekoden.
- `scripts/scan.ps1` kører sikkerhedsscanningen med opengrep før hver push, og værten kører den igen på hver pull request.

## Hvad vi fik ud af det

- Falske objekter slår mocks: en lille falsk motor er lettere at læse end en mock, der registrerer kald.
- En lokal scanning er ikke værtens scanning: værten brugte strengere regler og fandt to ting, som de lokale regler overså, så vi rettede dem og føjede et regelsæt til det lokale script.
- Skærmbilleder er en del af dokumentationen, så et lille værktøj tegner rigtigt kommandooutput som et SVG-billede uden at åbne et skrivebordsvindue.
