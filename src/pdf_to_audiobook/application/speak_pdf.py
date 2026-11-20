"""@brief The use case: read a PDF file aloud through the speakers."""

from collections.abc import Callable
from pathlib import Path

from pdf_to_audiobook.application.speak_text import speak_chunks
from pdf_to_audiobook.domain.errors import EmptyTextError
from pdf_to_audiobook.domain.speech import AudioPlayer, SpeechEngine
from pdf_to_audiobook.domain.text_chunks import split_text_into_chunks


def speak_pdf(
    pdf_path: str | Path,
    engine: SpeechEngine,
    player: AudioPlayer,
    extract_text: Callable[[Path], str],
    progress: Callable[[int, int], None] | None = None,
    should_stop: Callable[[], bool] | None = None,
) -> int:
    """!@brief Read the text of a PDF file aloud, chunk by chunk, in page order.

    @param pdf_path Path of the PDF file.
    @param engine The speech engine that speaks each chunk.
    @param player The player that plays each clip.
    @param extract_text Function that returns the text of a PDF file.
    @param progress Called as progress(done, total) after each played chunk.
    @param should_stop Asked before each chunk; True ends the speech early.
    @return The number of chunks spoken.
    @throws PdfTextError If the PDF text cannot be read (from extract_text).
    @throws EmptyTextError If the PDF text is blank.
    @throws SpeechEngineError If a chunk cannot be spoken (from the engine).
    @throws PlaybackError If a clip cannot be played (from the player).
    """
    chunks = split_text_into_chunks(extract_text(Path(pdf_path)))
    if not chunks:
        raise EmptyTextError(f"The PDF has no text to speak: {pdf_path}")
    return speak_chunks(chunks, engine, player, progress, should_stop)
