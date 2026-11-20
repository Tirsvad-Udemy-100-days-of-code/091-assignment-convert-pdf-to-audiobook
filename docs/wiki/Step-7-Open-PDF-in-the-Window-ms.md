[English](Step-7-Open-PDF-in-the-Window) · [Dansk](Step-7-Open-PDF-in-the-Window-da) · **Bahasa Malaysia**

# Langkah 7: Buka PDF dalam tetingkap

![Langkah 7: buka PDF dan dengarnya](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-07-open-pdf.svg)

## Apa yang kami lakukan

- Kami menambah butang Open PDF dan butang Stop pada tetingkap. Open PDF menunjukkan dialog fail untuk fail PDF, membaca teks dengan `pypdf` dan menyebutnya halaman demi halaman melalui pembesar suara.
- `speak_pdf(pdf_path, engine, player, extract_text)` ialah kes penggunaan. Pengekstrak teks dan pemilih fail disuntik, jadi kes penggunaan tidak pernah mengimport `pypdf` atau Tkinter dan ujian memilih fail tanpa dialog.
- `speak_text` dan `speak_pdf` berkongsi satu gelung, `speak_chunks`, jadi peraturan "semak Stop, sebut satu ketulan, mainkannya" wujud di satu tempat sahaja. Stop menamatkan pertuturan antara dua ketulan.
- PDF yang hilang, tidak boleh dibaca atau kosong dipaparkan sebagai mesej pada baris status, bukan sebagai traceback.

```powershell
pdf-to-audiobook-window
pwsh scripts/gui-test.ps1
```

- Ujian bekas membuka `tests/data/sample.pdf` melalui pemilih fail palsu pada paparan maya dan mencapai status Done (`pwsh scripts/gui-test.ps1`). Tangkapan skrin di atas datang daripadanya.
- Satu larian sebenar menyebut PDF contoh melalui pembesar suara: 2 ketulan, 23 saat, kod keluar 0.

## Apa yang kami peroleh

- Menyuntik pengekstrak dan pemilih memastikan tetingkap boleh diuji: hanya larian sebenar memerlukan dialog dan kad bunyi.
- Satu gelung untuk teks yang ditaip dan teks PDF bermakna Stop berfungsi untuk kedua-duanya dengan satu perubahan.
- `pypdf` hanya diimport apabila PDF dibuka, jadi tetingkap bermula pantas dan bekas hanya memerlukannya untuk ujian ini.
