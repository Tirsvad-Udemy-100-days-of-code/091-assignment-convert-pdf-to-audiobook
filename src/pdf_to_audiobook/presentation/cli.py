"""@brief Command line entry point and composition root."""

import argparse
import functools
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from pdf_to_audiobook.application.convert_pdf_to_audiobook import (
    convert_pdf_to_audiobook,
)
from pdf_to_audiobook.constants import (
    AUDIO_FILE_SUFFIX,
    DEFAULT_MODEL_NAME,
    EXIT_ERROR,
    EXIT_OK,
    EXIT_USAGE,
    PROGRAM_DESCRIPTION,
    PROGRAM_NAME,
    VERBOSE_HELP,
)
from pdf_to_audiobook.domain.errors import AudiobookError
from pdf_to_audiobook.domain.speech import SpeechEngine
from pdf_to_audiobook.infrastructure.coqui_engine import CoquiSpeechEngine
from pdf_to_audiobook.infrastructure.pdf_reader import extract_text_from_pdf


def main(
    argv: Sequence[str] | None = None,
    engine_factory: Callable[[str], SpeechEngine] | None = None,
) -> int:
    """!@brief Run the command line program.

    @param argv The arguments without the program name; defaults to sys.argv.
    @param engine_factory Builds an engine from a model name; defaults to Coqui
        (which honours --verbose).
    @return The exit code.
    """
    try:
        args = _build_parser().parse_args(argv)
    except SystemExit as exit_request:
        return EXIT_OK if exit_request.code in (0, None) else EXIT_USAGE
    factory = (
        engine_factory
        if engine_factory is not None
        else functools.partial(CoquiSpeechEngine, verbose=args.verbose)
    )
    pdf_path = Path(args.pdf)
    output_path = (
        Path(args.output) if args.output else pdf_path.with_suffix(AUDIO_FILE_SUFFIX)
    )
    try:
        result = convert_pdf_to_audiobook(
            pdf_path,
            output_path,
            factory(args.model),
            extract_text_from_pdf,
            _print_progress,
        )
    except AudiobookError as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_ERROR
    print(f"Wrote {result}")
    return EXIT_OK


def _build_parser() -> argparse.ArgumentParser:
    """!@brief Build the argument parser.

    @return The parser.
    """
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description=PROGRAM_DESCRIPTION)
    parser.add_argument("pdf", help="path of the PDF file to read")
    parser.add_argument(
        "-o",
        "--output",
        help=f"path of the {AUDIO_FILE_SUFFIX} file to write "
        "(default: the PDF path with that suffix)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_NAME,
        help="Coqui TTS model name (default: %(default)s)",
    )
    parser.add_argument("--verbose", action="store_true", help=VERBOSE_HELP)
    return parser


def _print_progress(done: int, total: int) -> None:
    """!@brief Tell the user which chunk is being finished.

    @param done Number of chunks spoken so far.
    @param total Number of chunks.
    @return Nothing.
    """
    print(f"Speaking chunk {done} of {total}", file=sys.stderr)
