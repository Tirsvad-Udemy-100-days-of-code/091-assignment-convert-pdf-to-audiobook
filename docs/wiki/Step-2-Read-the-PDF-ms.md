[English](Step-2-Read-the-PDF) · [Dansk](Step-2-Read-the-PDF-da) · **Bahasa Malaysia**

# Langkah 2: Baca PDF

![Langkah 2: baca PDF dan pecahkan teks](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-02-extract-text.svg)

## Apa yang kita lakukan

- `extract_text_from_pdf` membaca setiap halaman dengan `pypdf` dan menyambung teks halaman-halaman itu.
- `split_text_into_chunks` memotong teks pada hujung perenggan dan ayat kepada bahagian sepanjang paling banyak 400 aksara (`MAX_CHUNK_CHARS`), tidak pernah di tengah-tengah perkataan.
- PDF tanpa teks (contohnya imbasan) memberikan `PdfTextError` yang jelas, bukannya senyap.

```powershell
python tools/demo_extract.py tests/data/sample.pdf
```

## Apa yang kita perolehi

- Enjin suara berfungsi paling baik dengan bahagian teks yang pendek, jadi chunking ialah peraturan perniagaan yang sebenar, dan ia berada dalam lapisan domain tanpa input atau output.
- Ujian tidak memerlukan fail binari: fungsi pustaka standard yang kecil membina PDF yang sah secara langsung.
- Ralat dinamakan mengikut apa yang tidak kena, dan punca asal dikekalkan dengan `raise ... from`.
