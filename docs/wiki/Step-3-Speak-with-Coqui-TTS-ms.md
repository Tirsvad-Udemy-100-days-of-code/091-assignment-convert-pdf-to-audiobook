[English](Step-3-Speak-with-Coqui-TTS) · [Dansk](Step-3-Speak-with-Coqui-TTS-da) · **Bahasa Malaysia**

# Langkah 3: Bercakap dengan Coqui TTS

![Langkah 3: ucapkan satu ayat dengan Coqui TTS](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-03-coqui-tts.svg)

## Apa yang kita lakukan

- Menentukan satu port kecil, `SpeechEngine`, dengan satu kaedah: `synthesize(text)` memulangkan `AudioClip` (fail WAV dalam memori).
- Menulis `CoquiSpeechEngine` yang memuatkan model `tts_models/en/ljspeech/tacotron2-DCA` sekali sahaja, pada penggunaan pertama, dan mengimport Coqui TTS pada ketika itu sahaja.
- Meninggalkan perkhidmatan berbayar dalam tugasan (iSpeech, Google Cloud, Amazon Polly). Coqui TTS percuma, berjalan luar talian selepas muat turun model yang pertama dan kedengaran semula jadi.

```powershell
python tools/demo_speak.py "Coqui TTS turns this sentence into speech."
```

## Apa yang kita perolehi

- Port memastikan bahagian lain program bebas daripada enjin, jadi enjin lain hanyalah satu kelas baharu.
- Ujian lalai menggunakan enjin palsu (fake), jadi ia berjalan dalam sebahagian kecil saat dengan rangkaian disekat. Satu ujian bertanda `slow` menggunakan enjin sebenar (`python -m pytest -m slow`).
- Memilih model ialah pertukaran (trade-off): model `vits` memerlukan program sistem `espeak-ng`, manakala `tacotron2-DCA` hanya memerlukan pakej Python.
- Konsol kekal senyap: pustaka pertuturan mencetak teks fonem, amaran dan bar muat turun, jadi program menyembunyikannya dan hanya menunjukkan barisnya sendiri. Tambah `--verbose` pada arahan atau tetingkap untuk melihat output pustaka semula apabila anda menyiasat masalah. Ralat sebenar sentiasa dipaparkan.
