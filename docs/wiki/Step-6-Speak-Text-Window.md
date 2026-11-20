**English** · [Dansk](Step-6-Speak-Text-Window-da) · [Bahasa Malaysia](Step-6-Speak-Text-Window-ms)

# Step 6: The speak text window

![Step 6: type text and hear it](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-06-window.svg)

## What we did

- We added a small desktop window with a text box and a Speak button. The text is split into chunks, each chunk is spoken by Coqui TTS and played at once through the speakers with `sounddevice`.
- `speak_text(text, engine, player)` is the use case. The engine and the audio player are ports, so the use case never imports Tkinter, Coqui TTS or `sounddevice`.
- A view model holds the status and the busy flag; the Tkinter view only draws them and speaks on a worker thread so the window stays responsive. An error is shown as a message in the window, not as a traceback.

```powershell
pdf-to-audiobook-window
pwsh scripts/gui-test.ps1
```

- Run the window with `pdf-to-audiobook-window` or `python -m pdf_to_audiobook.presentation.window`.
- The window test runs in a Linux container on a virtual display (`pwsh scripts/gui-test.ps1`), so it never takes your mouse or keyboard. The screenshot above comes from that container.
- The real sound was checked once on a real output device: Coqui TTS plus `sounddevice` spoke a short sentence.

## What we gained

- A second port next to the speech port made the playback easy to replace in tests: no test makes a sound.
- A GUI is best tested in a container: the window, its log and its screenshot come back as files.
- Playback is one more dependency, so the decision is recorded in ADR-0002. On Linux the system needs `libportaudio2`.
- The console stays quiet: the speech library prints phoneme text, warnings and download bars, so the program hides them and shows only its own lines. Add `--verbose` to the command or to the window to see the library output again when you diagnose a problem. Real errors are always shown.
- The first sound takes several seconds because the voice model loads. The status line now says `Loading voice...` during that time, so the window no longer looks frozen. The engine reports the start of the load through one optional callback, and the window connects it to the status in its composition root only.
