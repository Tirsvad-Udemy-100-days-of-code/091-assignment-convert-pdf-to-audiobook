**English** · [Dansk](Step-3-Speak-with-Coqui-TTS-da) · [Bahasa Malaysia](Step-3-Speak-with-Coqui-TTS-ms)

# Step 3: Speak with Coqui TTS

![Step 3: speak a sentence with Coqui TTS](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-03-coqui-tts.svg)

## What we did

- Defined a small port, `SpeechEngine`, with one method: `synthesize(text)` returns an `AudioClip` (a WAV file in memory).
- Wrote `CoquiSpeechEngine` that loads the model `tts_models/en/ljspeech/tacotron2-DCA` once, on the first use, and imports Coqui TTS only then.
- Dropped the paid services of the assignment (iSpeech, Google Cloud, Amazon Polly). Coqui TTS is free, runs offline after the first model download and sounds natural.

```powershell
python tools/demo_speak.py "Coqui TTS turns this sentence into speech."
```

## What we gained

- A port keeps the rest of the program independent of the engine, so another engine is one new class.
- The default tests use a fake engine, so they run in a fraction of a second with the network blocked. One test marked `slow` uses the real engine (`python -m pytest -m slow`).
- Picking a model is a trade-off: the model `vits` needs the `espeak-ng` system program, while `tacotron2-DCA` needs only Python packages.
- The console stays quiet: the speech library prints phoneme text, warnings and download bars, so the program hides them and shows only its own lines. Add `--verbose` to the command or to the window to see the library output again when you diagnose a problem. Real errors are always shown.
