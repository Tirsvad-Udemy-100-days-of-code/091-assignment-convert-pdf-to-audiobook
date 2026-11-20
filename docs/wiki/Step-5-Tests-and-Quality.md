**English** · [Dansk](Step-5-Tests-and-Quality-da) · [Bahasa Malaysia](Step-5-Tests-and-Quality-ms)

# Step 5: Tests and quality

![Step 5: run the tests](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/091-assignment-convert-pdf-to-audiobook/raw/branch/main/docs/images/step-05-tests.svg)

## What we did

```powershell
python -m pytest
python -m pytest --cov=pdf_to_audiobook
python -m pytest -m slow
python -m ruff check src tests
python -m mypy
doxygen Doxyfile
pwsh scripts/scan.ps1
```

- 86 fast tests cover 99 percent of the source. A fixture blocks the network, so no test can reach the internet.
- `ruff` checks style, `mypy` in strict mode checks types, Doxygen builds the API documentation from the comments in the source.
- `scripts/scan.ps1` runs the opengrep security scan before every push, and the host runs it again on every pull request.

## What we gained

- Fakes beat mocks: a small fake engine is easier to read than a mock that records calls.
- A local scan is not the host's scan: the host used stricter rules and found two things the local rules missed, so we fixed them and added a rule set to the local script.
- Screenshots are part of the documentation, so a small tool renders real command output as an SVG image without opening a desktop window.
