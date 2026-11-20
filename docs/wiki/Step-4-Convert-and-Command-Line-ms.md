[English](Step-4-Convert-and-Command-Line) · [Dansk](Step-4-Convert-and-Command-Line-da) · **Bahasa Malaysia**

# Langkah 4: Tukar dan baris perintah

![Langkah 4: tukar PDF kepada buku audio](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-04-cli.svg)

## Apa yang kita lakukan

- `convert_pdf_to_audiobook(pdf_path, output_path, engine, extract_text, progress)` ialah fungsi tugasan: ekstrak, pecahkan, ucapkan setiap bahagian, sambung klip-klip dan tulis satu fail WAV.
- `join_wav_clips` menyambung klip dengan modul `wave` pustaka standard dan menolak klip yang mempunyai tetapan audio berbeza.
- Baris perintah ialah composition root: ia satu-satunya tempat yang membina enjin sebenar dan pembaca PDF sebenar.

```powershell
python -m pdf_to_audiobook tests/data/sample.pdf -o build/sample.wav
pdf-to-audiobook --help
```

Exit code: 0 berjaya, 1 ralat dengan mesej pada stderr, 2 penggunaan perintah yang salah.

## Apa yang kita perolehi

- Kebergantungan menghala ke dalam: use case mengenali port dan sebuah fungsi, bukan Coqui TTS atau `pypdf`.
- Kemajuan dan ralat dihantar ke stderr dan hasilnya ke stdout, jadi program ini berfungsi dalam skrip.
- Larian sebenar pada PDF sampel dua halaman menghasilkan kira-kira 17 saat suara.
- Konsol kekal senyap: pustaka pertuturan mencetak teks fonem, amaran dan bar muat turun, jadi program menyembunyikannya dan hanya menunjukkan barisnya sendiri. Tambah `--verbose` pada arahan atau tetingkap untuk melihat output pustaka semula apabila anda menyiasat masalah. Ralat sebenar sentiasa dipaparkan.
