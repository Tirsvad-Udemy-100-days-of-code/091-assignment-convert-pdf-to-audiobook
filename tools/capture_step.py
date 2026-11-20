"""@brief Render the real output of commands as an SVG terminal image.

The script runs each command, captures what it prints and draws it as a
terminal window in an SVG file. It needs no third-party package and opens no
window on the desktop, so it is safe to run on any machine and in a container.

Usage::

    python tools/capture_step.py --title "Step 1: setup" \
        --out docs/images/step-01-setup.svg \
        --cmd "python --version" --cmd "python -m pip --version"

@note The repository path and the home folder are replaced by ``<repo>`` and
      ``~`` so that no personal path ends up in the image.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

CHAR_WIDTH = 8.4
LINE_HEIGHT = 20
PADDING = 18
TITLE_BAR = 34
MAX_COLUMNS = 110
MAX_LINES = 40
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def _clean(text: str, replacements: dict[str, str]) -> str:
    """@brief Remove colour codes and hide personal paths.

    @param text Raw command output.
    @param replacements Map of text to hide and its replacement.
    @return The cleaned text.
    """
    text = ANSI_PATTERN.sub("", text).replace("\r", "")
    for needle, replacement in replacements.items():
        text = text.replace(needle, replacement)
    return text


def _wrap(line: str) -> list[str]:
    """@brief Cut one line at MAX_COLUMNS.

    @param line A line of text.
    @return One or more lines no longer than MAX_COLUMNS.
    """
    if len(line) <= MAX_COLUMNS:
        return [line]
    return [line[i : i + MAX_COLUMNS] for i in range(0, len(line), MAX_COLUMNS)]


def run_command(
    command: str, cwd: Path, replacements: dict[str, str]
) -> list[tuple[str, str]]:
    """@brief Run one command and return its lines for drawing.

    @param command Shell command line.
    @param cwd Folder to run in.
    @param replacements Text to hide in the output.
    @return Pairs of (kind, text) where kind is ``cmd`` or ``out``.
    """
    result = subprocess.run(  # noqa: S602 - the commands are written by the maintainer
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    lines: list[tuple[str, str]] = [("cmd", command)]
    output = _clean(result.stdout + result.stderr, replacements).rstrip("\n")
    for raw in output.split("\n") if output else []:
        lines.extend(("out", part) for part in _wrap(raw))
    return lines


def render_svg(title: str, lines: list[tuple[str, str]]) -> str:
    """@brief Draw lines as an SVG terminal window.

    @param title Text in the title bar.
    @param lines Pairs of (kind, text) from run_command.
    @return The SVG document as text.
    """
    if len(lines) > MAX_LINES:
        lines = [*lines[: MAX_LINES - 1], ("out", "... output shortened ...")]
    columns = max([len(title) + 6, *[len(text) + 2 for _, text in lines]])
    width = int(columns * CHAR_WIDTH + 2 * PADDING)
    height = TITLE_BAR + 2 * PADDING + LINE_HEIGHT * len(lines)
    rows = []
    for index, (kind, text) in enumerate(lines):
        y = TITLE_BAR + PADDING + LINE_HEIGHT * (index + 1) - 5
        if kind == "cmd":
            rows.append(
                f'<text x="{PADDING}" y="{y}" fill="#7ee787">$ </text>'
                f'<text x="{PADDING + 2 * CHAR_WIDTH:.1f}" y="{y}" fill="#e6edf3" '
                f'xml:space="preserve">{escape(text)}</text>'
            )
        else:
            rows.append(
                f'<text x="{PADDING}" y="{y}" fill="#c9d1d9" xml:space="preserve">'
                f"{escape(text)}</text>"
            )
    body = "\n  ".join(rows)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">\n'
        f'  <rect width="{width}" height="{height}" rx="8" fill="#0d1117"/>\n'
        f'  <rect width="{width}" height="{TITLE_BAR}" rx="8" fill="#161b22"/>\n'
        '  <circle cx="20" cy="17" r="6" fill="#ff5f56"/>\n'
        '  <circle cx="40" cy="17" r="6" fill="#ffbd2e"/>\n'
        '  <circle cx="60" cy="17" r="6" fill="#27c93f"/>\n'
        f'  <text x="{width / 2:.0f}" y="22" fill="#8b949e" text-anchor="middle" '
        'font-family="Consolas, Menlo, monospace" font-size="13">'
        f"{escape(title)}</text>\n"
        '  <g font-family="Consolas, Menlo, monospace" font-size="14">\n'
        f"  {body}\n  </g>\n</svg>\n"
    )


def main(argv: list[str] | None = None) -> int:
    """@brief Command line entry point.

    @param argv Arguments, or None for ``sys.argv``.
    @return Exit code: 0 when the image was written.
    """
    parser = argparse.ArgumentParser(
        description="Render command output as an SVG terminal."
    )
    parser.add_argument("--title", required=True, help="Text in the title bar")
    parser.add_argument("--out", required=True, type=Path, help="SVG file to write")
    parser.add_argument(
        "--cmd", action="append", required=True, help="Command to run (repeatable)"
    )
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help="Folder to run in")
    args = parser.parse_args(argv)

    cwd = args.cwd.resolve()
    replacements = {
        str(cwd): "<repo>",
        cwd.as_posix(): "<repo>",
        str(Path.home()): "~",
        Path.home().as_posix(): "~",
    }
    lines: list[tuple[str, str]] = []
    for command in args.cmd:
        lines.extend(run_command(command, cwd, replacements))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_svg(args.title, lines), encoding="utf-8", newline="\n")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
