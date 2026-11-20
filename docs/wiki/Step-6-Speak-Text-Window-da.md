[English](Step-6-Speak-Text-Window) · **Dansk** · [Bahasa Malaysia](Step-6-Speak-Text-Window-ms)

# Trin 6: Vinduet der læser tekst op

![Trin 6: skriv tekst og hør den](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-06-window.svg)

## Hvad vi gjorde

- Vi tilføjede et lille skrivebordsvindue med et tekstfelt og en Speak-knap. Teksten deles i bidder, hver bid læses op af Coqui TTS og afspilles med det samme i højttalerne med `sounddevice`.
- `speak_text(text, engine, player)` er anvendelsesfaldet. Motoren og lydafspilleren er porte, så anvendelsesfaldet importerer aldrig Tkinter, Coqui TTS eller `sounddevice`.
- En visningsmodel holder status og travl-flaget; Tkinter-visningen tegner dem kun og taler på en arbejdstråd, så vinduet forbliver responsivt. En fejl vises som en besked i vinduet, ikke som en traceback.

```powershell
pdf-to-audiobook-window
pwsh scripts/gui-test.ps1
```

- Start vinduet med `pdf-to-audiobook-window` eller `python -m pdf_to_audiobook.presentation.window`.
- Vinduestesten kører i en Linux-container på en virtuel skærm (`pwsh scripts/gui-test.ps1`), så den aldrig tager din mus eller dit tastatur. Skærmbilledet ovenfor kommer fra containeren.
- Den rigtige lyd blev tjekket én gang på en rigtig lydenhed: Coqui TTS og `sounddevice` sagde en kort sætning.

## Hvad vi fik ud af det

- En ekstra port ved siden af taleporten gjorde afspilningen nem at erstatte i tests: ingen test lager lyd.
- En grafisk brugerflade testes bedst i en container: vinduet, loggen og skærmbilledet kommer tilbage som filer.
- Afspilning er en afhængighed mere, så beslutningen står i ADR-0002. På Linux skal systemet have `libportaudio2`.
- Konsollen er rolig: talebiblioteket udskriver fonemtekst, advarsler og download-bjælker, så programmet skjuler dem og viser kun sine egne linjer. Tilføj `--verbose` til kommandoen eller til vinduet for at se bibliotekets output igen, når du søger fejl. Rigtige fejl vises altid.
