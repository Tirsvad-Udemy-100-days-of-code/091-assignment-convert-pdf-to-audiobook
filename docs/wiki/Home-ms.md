[English](Home) · [Dansk](Home-da) · **Bahasa Malaysia**

# PDF kepada Buku Audio

Satu program Python 3.13 yang kecil yang membaca fail PDF dan menukar teksnya kepada suara, supaya anda mendapat buku audio percuma. Ini ialah tugasan Hari ke-91 kursus Udemy *100 Days of Code: The Complete Python Pro Bootcamp*.

Tugasan itu mencadangkan perkhidmatan web teks-ke-suara yang berbayar. Projek ini tidak membayar apa-apa: ia menggunakan [Coqui TTS](https://github.com/idiap/coqui-ai-TTS), enjin suara sumber terbuka yang berjalan pada komputer anda sendiri.

## Lima langkah kuliah

Setiap langkah mempunyai satu halaman yang menunjukkan tangkapan skrin dan menerangkan apa yang kita perolehi.

| Langkah | Halaman | Apa itu |
| --- | --- | --- |
| 1 | [Langkah 1: Persekitaran](Step-1-Environment-ms) | `.venv` setempat, pip dinaik taraf, projek dipasang |
| 2 | [Langkah 2: Baca PDF](Step-2-Read-the-PDF-ms) | Ekstrak teks dan pecahkannya kepada bahagian-bahagian |
| 3 | [Langkah 3: Bercakap dengan Coqui TTS](Step-3-Speak-with-Coqui-TTS-ms) | Tukar satu bahagian teks kepada audio |
| 4 | [Langkah 4: Tukar dan baris perintah](Step-4-Convert-and-Command-Line-ms) | Keseluruhan penukaran dari terminal |
| 5 | [Langkah 5: Ujian dan kualiti](Step-5-Tests-and-Quality-ms) | Ujian, jenis data, gaya kod dan imbasan keselamatan |
| 6 | [Langkah 6: Tetingkap bacaan teks](Step-6-Speak-Text-Window-ms) | Taip teks dan dengar melalui pembesar suara |
| 7 | [Langkah 7: Buka PDF dalam tetingkap](Step-7-Open-PDF-in-the-Window-ms) | Buka PDF dan dengarnya, dengan butang Stop |

Baca juga [Reka bentuk](Design-ms) untuk melihat bagaimana kod dilapiskan dan [Refleksi](Reflection-ms) untuk apa yang kita pelajari.

## Mula pantas

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pdf_to_audiobook tests/data/sample.pdf -o build/sample.wav
```

Pemasangan pertama dan larian pertama memuat turun beberapa ratus megabait (PyTorch dan model suara).
