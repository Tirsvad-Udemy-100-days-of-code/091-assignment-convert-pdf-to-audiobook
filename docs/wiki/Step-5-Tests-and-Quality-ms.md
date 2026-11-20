[English](Step-5-Tests-and-Quality) · [Dansk](Step-5-Tests-and-Quality-da) · **Bahasa Malaysia**

# Langkah 5: Ujian dan kualiti

![Langkah 5: jalankan ujian](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-05-tests.svg)

## Apa yang kita lakukan

```powershell
python -m pytest
python -m pytest --cov=pdf_to_audiobook
python -m pytest -m slow
python -m ruff check src tests
python -m mypy
doxygen Doxyfile
pwsh scripts/scan.ps1
```

- 110 ujian pantas meliputi 98 peratus kod sumber. Satu fixture menyekat rangkaian, jadi tiada ujian yang boleh mencapai internet.
- `ruff` menyemak gaya kod, `mypy` dalam mod strict menyemak jenis data, dan Doxygen membina dokumentasi API daripada komen dalam kod sumber.
- `scripts/scan.ps1` menjalankan imbasan keselamatan opengrep sebelum setiap push, dan hos menjalankannya sekali lagi pada setiap pull request.

## Apa yang kita perolehi

- Fake lebih baik daripada mock: enjin palsu yang kecil lebih mudah dibaca daripada mock yang merekodkan panggilan.
- Imbasan setempat bukan imbasan hos: hos menggunakan peraturan yang lebih ketat dan menemui dua perkara yang terlepas daripada peraturan setempat, jadi kita membetulkannya dan menambah set peraturan pada skrip setempat.
- Tangkapan skrin ialah sebahagian daripada dokumentasi, jadi alat kecil memaparkan output perintah sebenar sebagai imej SVG tanpa membuka tetingkap desktop.
