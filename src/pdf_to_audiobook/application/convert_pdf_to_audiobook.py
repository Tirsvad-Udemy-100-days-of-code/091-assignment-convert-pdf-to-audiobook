"""@brief The use case: turn a PDF file into an audiobook file."""

from collections.abc import Callable
from pathlib import Path

from pdf_to_audiobook.constants import AUDIO_FILE_SUFFIX
from pdf_to_audiobook.domain.audio_join import join_wav_clips
from pdf_to_audiobook.domain.errors import AudiobookError, OutputWriteError
from pdf_to_audiobook.domain.speech import AudioClip, SpeechEngine
from pdf_to_audiobook.domain.text_chunks import split_text_into_chunks


def convert_pdf_to_audiobook(
    pdf_path: str | Path,
    output_path: str | Path,
    engine: SpeechEngine,
    extract_text: Callable[[Path], str],
    progress: Callable[[int, int], None] | None = None,
) -> Path:
    """!@brief Read a PDF file aloud and save the speech as one WAV file.

    @param pdf_path Path of the PDF file.
    @param output_path Path of the WAV file to write; its folder is created.
    @param engine The speech engine that speaks each chunk.
    @param extract_text Function that returns the text of a PDF file.
    @param progress Called as progress(done, total) after each spoken chunk.
    @return The path of the WAV file.
    @throws AudiobookError If the suffix is wrong, the text has no chunks or
        the audio cannot be written.
    @throws PdfTextError If the PDF text cannot be read (from extract_text).
    @throws SpeechEngineError If a chunk cannot be spoken (from the engine).
    """
    output = Path(output_path)
    if output.suffix.lower() != AUDIO_FILE_SUFFIX:
        raise AudiobookError(
            f"Output file must end with {AUDIO_FILE_SUFFIX}, got {output.name!r}."
        )
    chunks = split_text_into_chunks(extract_text(Path(pdf_path)))
    if not chunks:
        raise AudiobookError(f"The PDF has no text to speak: {pdf_path}")
    clips = _speak_chunks(chunks, engine, progress)
    _write_audio(output, join_wav_clips(clips))
    return output


def _speak_chunks(
    chunks: list[str],
    engine: SpeechEngine,
    progress: Callable[[int, int], None] | None,
) -> list[AudioClip]:
    """!@brief Speak every chunk in order and report progress.

    @param chunks The text chunks.
    @param engine The speech engine.
    @param progress Optional progress callback.
    @return One clip per chunk.
    """
    clips: list[AudioClip] = []
    for done, chunk in enumerate(chunks, start=1):
        clips.append(engine.synthesize(chunk))
        if progress is not None:
            progress(done, len(chunks))
    return clips


def _write_audio(output: Path, clip: AudioClip) -> None:
    """!@brief Write a clip to a file, creating its folder.

    @param output Path of the file.
    @param clip The clip to write.
    @return Nothing.
    @throws OutputWriteError If the file cannot be written.
    """
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(clip.data)
    except OSError as error:
        raise OutputWriteError(f"Cannot write {output}: {error}") from error
