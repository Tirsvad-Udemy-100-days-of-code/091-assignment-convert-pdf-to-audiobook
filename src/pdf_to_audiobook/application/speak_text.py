"""@brief The use case: speak a text through the speakers."""

from collections.abc import Callable

from pdf_to_audiobook.domain.errors import EmptyTextError
from pdf_to_audiobook.domain.speech import AudioPlayer, SpeechEngine
from pdf_to_audiobook.domain.text_chunks import split_text_into_chunks


def speak_text(
    text: str,
    engine: SpeechEngine,
    player: AudioPlayer,
    progress: Callable[[int, int], None] | None = None,
    should_stop: Callable[[], bool] | None = None,
) -> int:
    """!@brief Speak a text chunk by chunk, in order.

    @param text The text to speak.
    @param engine The speech engine that speaks each chunk.
    @param player The player that plays each clip.
    @param progress Called as progress(done, total) after each played chunk.
    @param should_stop Asked before each chunk; True ends the speech early.
    @return The number of chunks spoken.
    @throws EmptyTextError If the text is blank.
    @throws SpeechEngineError If a chunk cannot be spoken (from the engine).
    @throws PlaybackError If a clip cannot be played (from the player).
    """
    chunks = split_text_into_chunks(text.strip())
    if not chunks:
        raise EmptyTextError("There is no text to speak.")
    return speak_chunks(chunks, engine, player, progress, should_stop)


def speak_chunks(
    chunks: list[str],
    engine: SpeechEngine,
    player: AudioPlayer,
    progress: Callable[[int, int], None] | None = None,
    should_stop: Callable[[], bool] | None = None,
) -> int:
    """!@brief Synthesize and play each chunk in order, stopping when asked.

    @param chunks The text chunks to speak.
    @param engine The speech engine that speaks each chunk.
    @param player The player that plays each clip.
    @param progress Called as progress(done, total) after each played chunk.
    @param should_stop Asked before each chunk; True ends the speech early.
    @return The number of chunks spoken.
    @throws SpeechEngineError If a chunk cannot be spoken (from the engine).
    @throws PlaybackError If a clip cannot be played (from the player).
    """
    done = 0
    for chunk in chunks:
        if should_stop is not None and should_stop():
            break
        player.play(engine.synthesize(chunk))
        done += 1
        if progress is not None:
            progress(done, len(chunks))
    return done
