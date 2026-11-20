import pytest

from pdf_to_audiobook.constants import MAX_CHUNK_CHARS
from pdf_to_audiobook.domain.text_chunks import split_text_into_chunks


@pytest.mark.parametrize("text", ["", "   ", "\n\n \t\n"])
def test_split_returns_empty_list_for_blank_text(text: str) -> None:
    assert split_text_into_chunks(text) == []


def test_split_keeps_one_sentence_in_one_chunk() -> None:
    assert split_text_into_chunks("Hello world.") == ["Hello world."]


def test_split_packs_many_sentences_greedily() -> None:
    text = "One two. Three four. Five six. Seven eight."
    assert split_text_into_chunks(text, max_chars=22) == [
        "One two. Three four.",
        "Five six. Seven eight.",
    ]


def test_split_collapses_whitespace_runs() -> None:
    assert split_text_into_chunks("Hello \n  world.\tOk!") == ["Hello world. Ok!"]


def test_split_starts_new_chunk_at_paragraph_break() -> None:
    assert split_text_into_chunks("First one.\n\nSecond one.") == [
        "First one.",
        "Second one.",
    ]


def test_split_accepts_chunk_of_exactly_max_chars() -> None:
    assert split_text_into_chunks("abcd efgh", max_chars=9) == ["abcd efgh"]


def test_split_breaks_when_chunk_would_exceed_max_chars_by_one() -> None:
    assert split_text_into_chunks("abcd efgh", max_chars=8) == ["abcd", "efgh"]


def test_split_cuts_overlong_sentence_between_words() -> None:
    text = "alpha beta gamma delta epsilon"
    chunks = split_text_into_chunks(text, max_chars=12)
    assert chunks == ["alpha beta", "gamma delta", "epsilon"]


def test_split_cuts_overlong_word_into_pieces() -> None:
    assert split_text_into_chunks("abcdefghij", max_chars=4) == [
        "abcd",
        "efgh",
        "ij",
    ]


def test_split_keeps_non_ascii_text() -> None:
    text = "Blåbærgrød æder åen. Naïve café!"
    assert split_text_into_chunks(text) == [text]
    assert split_text_into_chunks(text, max_chars=21) == [
        "Blåbærgrød æder åen.",
        "Naïve café!",
    ]


@pytest.mark.parametrize("max_chars", [0, -1])
def test_split_rejects_max_chars_below_one(max_chars: int) -> None:
    with pytest.raises(ValueError, match="max_chars"):
        split_text_into_chunks("text", max_chars=max_chars)


def test_split_never_exceeds_limit_or_cuts_words() -> None:
    text = ("Lorem ipsum dolor sit amet, consectetur! " * 30 + "\n\n") * 3
    words = set(text.split())
    for max_chars in (12, 25, 80, MAX_CHUNK_CHARS):
        chunks = split_text_into_chunks(text, max_chars=max_chars)
        assert all(0 < len(chunk) <= max_chars for chunk in chunks)
        assert {word for chunk in chunks for word in chunk.split()} <= words
        assert " ".join(chunks).split() == text.split()
