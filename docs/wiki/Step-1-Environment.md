**English** · [Dansk](Step-1-Environment-da) · [Bahasa Malaysia](Step-1-Environment-ms)

# Step 1: Environment

![Step 1: create the .venv and upgrade pip](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-01-setup.svg)

## What we did

1. Created a local virtual environment in `.venv` so the project's packages do not touch the system Python.
2. Upgraded pip with `python -m pip install --upgrade pip`.
3. Installed the project in editable mode with the development tools: `python -m pip install -e ".[dev]"`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Linux and macOS use `python3 -m venv .venv` and `source .venv/bin/activate`.

## What we gained

- A repeatable setup: everything the project needs is declared in `pyproject.toml`, so one command installs it.
- A clean separation between the project and the system Python.
- The knowledge that the heavy part is the speech engine: Coqui TTS needs PyTorch, so the first install is large.
