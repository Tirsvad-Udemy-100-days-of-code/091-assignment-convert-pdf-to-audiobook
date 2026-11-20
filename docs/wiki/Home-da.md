[English](Home) · **Dansk** · [Bahasa Malaysia](Home-ms)

# PDF til lydbog

Et lille Python 3.13-program, der læser en PDF-fil og omdanner teksten til tale, så du får en gratis lydbog. Det er opgaven fra dag 91 på Udemy-kurset *100 Days of Code: The Complete Python Pro Bootcamp*.

Opgaven foreslår betalte tale-web-tjenester. Dette projekt betaler for ingenting: det bruger [Coqui TTS](https://github.com/idiap/coqui-ai-TTS), en talemotor med åben kildekode, der kører på din egen maskine.

## De fem trin fra lektionen

Hvert trin har en side med et skærmbillede og en forklaring af, hvad vi fik ud af det.

| Trin | Side | Hvad det er |
| --- | --- | --- |
| 1 | [Trin 1: Miljø](Step-1-Environment-da) | Et lokalt `.venv`, pip opgraderet, projektet installeret |
| 2 | [Trin 2: Læs PDF'en](Step-2-Read-the-PDF-da) | Træk teksten ud og del den i stykker |
| 3 | [Trin 3: Tal med Coqui TTS](Step-3-Speak-with-Coqui-TTS-da) | Omdan et stykke tekst til lyd |
| 4 | [Trin 4: Konvertering og kommandolinje](Step-4-Convert-and-Command-Line-da) | Hele konverteringen fra en terminal |
| 5 | [Trin 5: Tests og kvalitet](Step-5-Tests-and-Quality-da) | Tests, typer, stil og sikkerhedsscanningen |
| 6 | [Trin 6: Vinduet der læser tekst op](Step-6-Speak-Text-Window-da) | Skriv tekst og hør den i højttalerne |

Læs også [Design](Design-da) om, hvordan koden er opdelt i lag, og [Refleksion](Reflection-da) om, hvad vi lærte.

## Hurtig start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pdf_to_audiobook tests/data/sample.pdf -o build/sample.wav
```

Den første installation og den første kørsel henter flere hundrede megabyte (PyTorch og stemmemodellen).
