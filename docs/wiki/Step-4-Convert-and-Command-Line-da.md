[English](Step-4-Convert-and-Command-Line) · **Dansk** · [Bahasa Malaysia](Step-4-Convert-and-Command-Line-ms)

# Trin 4: Konvertering og kommandolinje

![Trin 4: konvertér en PDF til en lydbog](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-04-cli.svg)

## Hvad vi gjorde

- `convert_pdf_to_audiobook(pdf_path, output_path, engine, extract_text, progress)` er opgavens funktion: træk teksten ud, del den, læs hvert stykke op, sæt klippene sammen og skriv én WAV-fil.
- `join_wav_clips` sætter klippene sammen med standardbibliotekets `wave`-modul og afviser klip med forskellige lydindstillinger.
- Kommandolinjen er kompositionsroden: den er det eneste sted, der bygger den rigtige motor og den rigtige PDF-læser.

```powershell
python -m pdf_to_audiobook tests/data/sample.pdf -o build/sample.wav
pdf-to-audiobook --help
```

Afslutningskoder: 0 succes, 1 en fejl med en besked på stderr, 2 forkert brug af kommandoen.

## Hvad vi fik ud af det

- Afhængigheder peger indad: brugstilfældet kender porten og en funktion, ikke Coqui TTS eller `pypdf`.
- Fremdrift og fejl går til stderr og resultatet til stdout, så programmet fungerer i scripts.
- En rigtig kørsel på den to sider lange eksempel-PDF gav omkring 17 sekunders tale.
