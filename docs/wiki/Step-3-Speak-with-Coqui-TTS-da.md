[English](Step-3-Speak-with-Coqui-TTS) · **Dansk** · [Bahasa Malaysia](Step-3-Speak-with-Coqui-TTS-ms)

# Trin 3: Tal med Coqui TTS

![Trin 3: sig en sætning med Coqui TTS](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-03-coqui-tts.svg)

## Hvad vi gjorde

- Definerede en lille port, `SpeechEngine`, med én metode: `synthesize(text)` returnerer en `AudioClip` (en WAV-fil i hukommelsen).
- Skrev `CoquiSpeechEngine`, der indlæser modellen `tts_models/en/ljspeech/tacotron2-DCA` én gang, ved første brug, og først da importerer Coqui TTS.
- Droppede opgavens betalte tjenester (iSpeech, Google Cloud, Amazon Polly). Coqui TTS er gratis, kører offline efter den første modeldownload og lyder naturlig.

```powershell
python tools/demo_speak.py "Coqui TTS turns this sentence into speech."
```

## Hvad vi fik ud af det

- En port holder resten af programmet uafhængigt af motoren, så en anden motor blot er én ny klasse.
- Standardtestene bruger en falsk motor, så de kører på brøkdele af et sekund med netværket blokeret. Én test markeret `slow` bruger den rigtige motor (`python -m pytest -m slow`).
- Valg af model er en afvejning: modellen `vits` kræver systemprogrammet `espeak-ng`, mens `tacotron2-DCA` kun kræver Python-pakker.
- Konsollen er rolig: talebiblioteket udskriver fonemtekst, advarsler og download-bjælker, så programmet skjuler dem og viser kun sine egne linjer. Tilføj `--verbose` til kommandoen eller til vinduet for at se bibliotekets output igen, når du søger fejl. Rigtige fejl vises altid.
