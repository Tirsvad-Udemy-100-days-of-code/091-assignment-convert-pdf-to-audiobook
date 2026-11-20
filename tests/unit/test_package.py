import importlib

import pytest

import pdf_to_audiobook
from pdf_to_audiobook import constants


def test_package_imports() -> None:
    assert importlib.import_module("pdf_to_audiobook") is pdf_to_audiobook


def test_version_is_initial_release() -> None:
    assert pdf_to_audiobook.__version__ == "0.1.0"


def test_constants_have_stated_values() -> None:
    assert constants.PACKAGE_NAME == "pdf_to_audiobook"
    assert constants.MAX_CHUNK_CHARS == 400
    assert constants.AUDIO_FILE_SUFFIX == ".wav"
    assert constants.EXIT_OK == 0
    assert constants.EXIT_ERROR == 1
    assert constants.EXIT_USAGE == 2


def test_exit_codes_are_distinct() -> None:
    codes = {constants.EXIT_OK, constants.EXIT_ERROR, constants.EXIT_USAGE}
    assert len(codes) == 3


@pytest.mark.parametrize(
    "layer", ["domain", "application", "infrastructure", "presentation"]
)
def test_layer_packages_import(layer: str) -> None:
    module = importlib.import_module(f"pdf_to_audiobook.{layer}")
    assert module.__doc__
