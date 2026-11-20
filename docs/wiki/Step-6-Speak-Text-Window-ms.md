[English](Step-6-Speak-Text-Window) · [Dansk](Step-6-Speak-Text-Window-da) · **Bahasa Malaysia**

# Langkah 6: Tetingkap bacaan teks

![Langkah 6: taip teks dan dengarnya](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-06-window.svg)

## Apa yang kami lakukan

- Kami menambah tetingkap desktop kecil dengan kotak teks dan butang Speak. Teks dipecahkan kepada ketulan, setiap ketulan dibaca oleh Coqui TTS dan terus dimainkan melalui pembesar suara dengan `sounddevice`.
- `speak_text(text, engine, player)` ialah kes penggunaan. Enjin dan pemain audio ialah port, jadi kes penggunaan tidak pernah mengimport Tkinter, Coqui TTS atau `sounddevice`.
- Satu model paparan menyimpan status dan bendera sibuk; paparan Tkinter hanya melukisnya dan bercakap pada benang pekerja supaya tetingkap kekal responsif. Ralat dipaparkan sebagai mesej dalam tetingkap, bukan sebagai traceback.

```powershell
pdf-to-audiobook-window
pwsh scripts/gui-test.ps1
```

- Jalankan tetingkap dengan `pdf-to-audiobook-window` atau `python -m pdf_to_audiobook.presentation.window`.
- Ujian tetingkap berjalan dalam bekas Linux pada paparan maya (`pwsh scripts/gui-test.ps1`), jadi ia tidak pernah mengambil tetikus atau papan kekunci anda. Tangkapan skrin di atas datang daripada bekas itu.
- Bunyi sebenar disemak sekali pada peranti output sebenar: Coqui TTS dan `sounddevice` menyebut satu ayat pendek.

## Apa yang kami peroleh

- Satu port tambahan di sebelah port pertuturan menjadikan pemainan mudah diganti dalam ujian: tiada ujian yang mengeluarkan bunyi.
- Antara muka grafik paling baik diuji dalam bekas: tetingkap, log dan tangkapan skrin kembali sebagai fail.
- Pemainan ialah satu kebergantungan lagi, jadi keputusan itu dicatat dalam ADR-0002. Pada Linux sistem memerlukan `libportaudio2`.
