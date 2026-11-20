"""@brief Split text into chunks small enough for the speech engine."""

import re

from pdf_to_audiobook.constants import (
    MAX_CHUNK_CHARS,
    PARAGRAPH_BREAK_PATTERN,
    SENTENCE_BREAK_PATTERN,
)


def split_text_into_chunks(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """!@brief Split text into chunks of at most max_chars characters.

    Text is split on paragraph breaks, then on sentence ends. Whole sentences
    are packed into a chunk; a chunk never spans two paragraphs. Runs of
    whitespace become one space. A sentence longer than max_chars is split
    between words, and a word longer than max_chars is cut into pieces.

    @param text The text to split.
    @param max_chars The largest number of characters in one chunk.
    @return The chunks in reading order; empty when the text has no words.
    @throws ValueError If max_chars is less than 1.
    """
    if max_chars < 1:
        raise ValueError(f"max_chars must be at least 1, got {max_chars}")
    chunks: list[str] = []
    for paragraph in re.split(PARAGRAPH_BREAK_PATTERN, text):
        sentences = re.split(SENTENCE_BREAK_PATTERN, _collapse_whitespace(paragraph))
        chunks.extend(_pack_pieces(_pieces_of(sentences, max_chars), max_chars))
    return chunks


def _collapse_whitespace(text: str) -> str:
    """!@brief Replace each run of whitespace by one space.

    @param text The text to clean.
    @return The text with single spaces and no outer whitespace.
    """
    return " ".join(text.split())


def _pieces_of(sentences: list[str], max_chars: int) -> list[str]:
    """!@brief Turn sentences into pieces no longer than max_chars.

    @param sentences The sentences of one paragraph.
    @param max_chars The largest number of characters in one piece.
    @return The sentences, with an overlong one split between words.
    """
    pieces: list[str] = []
    for sentence in sentences:
        if not sentence:
            continue
        if len(sentence) <= max_chars:
            pieces.append(sentence)
        else:
            pieces.extend(_pack_pieces(_split_words(sentence, max_chars), max_chars))
    return pieces


def _split_words(sentence: str, max_chars: int) -> list[str]:
    """!@brief Split a sentence into words, cutting a word longer than max_chars.

    @param sentence The sentence to split.
    @param max_chars The largest number of characters in one word piece.
    @return The words in order.
    """
    words: list[str] = []
    for word in sentence.split(" "):
        words.extend(word[i : i + max_chars] for i in range(0, len(word), max_chars))
    return words


def _pack_pieces(pieces: list[str], max_chars: int) -> list[str]:
    """!@brief Join pieces with a space into chunks of at most max_chars.

    @param pieces The pieces, each at most max_chars long.
    @param max_chars The largest number of characters in one chunk.
    @return The chunks in order.
    """
    chunks: list[str] = []
    current = ""
    for piece in pieces:
        if current and len(current) + 1 + len(piece) <= max_chars:
            current = f"{current} {piece}"
        else:
            if current:
                chunks.append(current)
            current = piece
    if current:
        chunks.append(current)
    return chunks
