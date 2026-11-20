[English](Step-1-Environment) · **Dansk** · [Bahasa Malaysia](Step-1-Environment-ms)

# Trin 1: Miljø

![Trin 1: opret .venv og opgrader pip](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-01-setup.svg)

## Hvad vi gjorde

1. Oprettede et lokalt virtuelt miljø i `.venv`, så projektets pakker ikke rører systemets Python.
2. Opgraderede pip med `python -m pip install --upgrade pip`.
3. Installerede projektet i redigerbar tilstand sammen med udviklingsværktøjerne: `python -m pip install -e ".[dev]"`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

På Linux og macOS bruges `python3 -m venv .venv` og `source .venv/bin/activate`.

## Hvad vi fik ud af det

- En opsætning, der kan gentages: alt, hvad projektet har brug for, er angivet i `pyproject.toml`, så én kommando installerer det hele.
- En ren adskillelse mellem projektet og systemets Python.
- Viden om, at den tunge del er talemotoren: Coqui TTS kræver PyTorch, så den første installation er stor.
