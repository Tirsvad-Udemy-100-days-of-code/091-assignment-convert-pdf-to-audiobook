"""Start the real window with fakes and check that it speaks; for the container."""

import argparse
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

from tests.fakes import FakeFileChooser, FakePlayer, FakeSpeechEngine  # noqa: E402

from pdf_to_audiobook.constants import STATUS_DONE  # noqa: E402
from pdf_to_audiobook.presentation.window import main  # noqa: E402

SCRIPT_TEXT = "Hello from the window test. This is the second sentence."


def run(log_path: Path, hold: float, pdf: Path | None) -> int:
    """Run the window with fakes, write one log line and return the exit code.

    With a PDF path, a fake file chooser returns it and Open PDF is pressed;
    otherwise the script text is typed and Speak is pressed.
    """
    engine = FakeSpeechEngine()
    player = FakePlayer()
    started = time.monotonic()
    chooser = FakeFileChooser(pdf)
    arguments = ["--open-pdf"] if pdf is not None else ["--script", SCRIPT_TEXT]
    code = main(
        [*arguments, "--hold", str(hold)],
        engine_factory=lambda _model: engine,
        player_factory=lambda: player,
        chooser_factory=lambda: chooser,
    )
    seconds = time.monotonic() - started
    ok = code == 0 and bool(player.clips)
    status = STATUS_DONE if ok else "failed"
    mode = "open-pdf" if pdf is not None else "speak"
    line = (
        f"status={status} mode={mode} exit_code={code} chunks={len(player.clips)} "
        f"texts={engine.texts!r} seconds={seconds:.1f}"
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="\n") as log:
        log.write(line + "\n")
    print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, required=True, help="log file to append")
    parser.add_argument(
        "--pdf", type=Path, help="PDF file the fake file chooser returns"
    )
    parser.add_argument("--hold", type=float, default=0.0, help="seconds to stay open")
    options = parser.parse_args()
    sys.exit(run(options.log, options.hold, options.pdf))
