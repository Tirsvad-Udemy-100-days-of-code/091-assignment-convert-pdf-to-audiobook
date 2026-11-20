[English](Step-1-Environment) · [Dansk](Step-1-Environment-da) · **Bahasa Malaysia**

# Langkah 1: Persekitaran

![Langkah 1: cipta .venv dan naik taraf pip](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-01-setup.svg)

## Apa yang kita lakukan

1. Mencipta virtual environment setempat dalam `.venv` supaya pakej projek tidak menyentuh Python sistem.
2. Menaik taraf pip dengan `python -m pip install --upgrade pip`.
3. Memasang projek dalam mod editable bersama alat pembangunan: `python -m pip install -e ".[dev]"`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Pada Linux dan macOS, gunakan `python3 -m venv .venv` dan `source .venv/bin/activate`.

## Apa yang kita perolehi

- Persediaan yang boleh diulang: semua yang diperlukan projek diisytiharkan dalam `pyproject.toml`, jadi satu perintah memasang semuanya.
- Pengasingan yang bersih antara projek dan Python sistem.
- Pengetahuan bahawa bahagian yang berat ialah enjin suara: Coqui TTS memerlukan PyTorch, jadi pemasangan pertama adalah besar.
