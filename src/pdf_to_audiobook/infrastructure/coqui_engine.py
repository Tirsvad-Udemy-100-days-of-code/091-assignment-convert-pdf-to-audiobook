"""@brief Speech engine that runs Coqui TTS on this computer."""

import tempfile
import wave
from collections.abc import Callable
from pathlib import Path
from typing import Protocol

from pdf_to_audiobook.constants import (
    DEFAULT_MODEL_NAME,
    INSTALL_COMMAND,
    MAX_CHUNK_CHARS,
    SPEECH_TEMP_FILE_NAME,
)
from pdf_to_audiobook.domain.errors import EngineUnavailableError, SpeechEngineError
from pdf_to_audiobook.domain.speech import AudioClip
from pdf_to_audiobook.infrastructure.quiet_output import quiet_output


class TtsModel(Protocol):
    """!@brief The part of a Coqui TTS model the engine uses."""

    def tts_to_file(self, *, text: str, file_path: str) -> object:
        """!@brief Speak text into a WAV file.

        @param text The text to speak.
        @param file_path Path of the WAV file to write.
        @return Whatever the model returns; the engine ignores it.
        """
        ...


## A function that loads the model with the given name.
TtsLoader = Callable[[str], TtsModel]


def load_coqui_model(model_name: str) -> TtsModel:
    """!@brief Load a Coqui TTS model, downloading it on first use.

    @param model_name Name of the model, for example tts_models/en/ljspeech/....
    @return The loaded model.
    @throws EngineUnavailableError If Coqui TTS is not installed or the model fails.
    """
    try:
        # Imported here, not at module level: TTS pulls in torch and is slow.
        from TTS.api import TTS
    except ImportError as error:
        raise EngineUnavailableError(
            f"Coqui TTS is not installed. Install the project with: {INSTALL_COMMAND}"
        ) from error
    try:
        model: TtsModel = TTS(model_name)
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        raise EngineUnavailableError(
            f"Cannot load the speech model {model_name!r}: {error}"
        ) from error
    return model


class CoquiSpeechEngine:
    """!@brief SpeechEngine that uses a local Coqui TTS model."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        loader: TtsLoader | None = None,
        verbose: bool = False,
    ) -> None:
        """!@brief Create the engine without loading the model.

        @param model_name Name of the Coqui TTS model to use.
        @param loader Function that loads a model; defaults to the real Coqui TTS.
        @param verbose True shows the console output of the library.
        """
        ## Name of the model to load.
        self._model_name = model_name
        ## Function that loads the model.
        self._loader: TtsLoader = loader if loader is not None else load_coqui_model
        ## True when the output of the library is shown.
        self._verbose = verbose
        ## The loaded model; None until the first call.
        self._model: TtsModel | None = None

    def synthesize(self, text: str) -> AudioClip:
        """!@brief Speak one piece of text.

        @param text The text to speak, not empty and at most MAX_CHUNK_CHARS long.
        @return The spoken text as a WAV clip.
        @throws SpeechEngineError If the text is invalid or synthesis fails.
        @throws EngineUnavailableError If the model cannot be loaded.
        """
        _check_text(text)
        model = self._get_model()
        with tempfile.TemporaryDirectory() as folder:
            wav_path = Path(folder) / SPEECH_TEMP_FILE_NAME
            try:
                with quiet_output(not self._verbose):
                    model.tts_to_file(text=text, file_path=str(wav_path))
            except (OSError, RuntimeError, ValueError, KeyError) as error:
                raise SpeechEngineError(f"Speech synthesis failed: {error}") from error
            return _read_clip(wav_path)

    def _get_model(self) -> TtsModel:
        """!@brief Return the model, loading it on the first call only.

        @return The loaded model.
        """
        if self._model is None:
            with quiet_output(not self._verbose):
                self._model = self._loader(self._model_name)
        return self._model


def _check_text(text: str) -> None:
    """!@brief Reject text the engine cannot speak.

    @param text The text to check.
    @return Nothing; the text is valid when no error is raised.
    @throws SpeechEngineError If the text is blank or longer than MAX_CHUNK_CHARS.
    """
    if not text.strip():
        raise SpeechEngineError("There is no text to speak.")
    if len(text) > MAX_CHUNK_CHARS:
        raise SpeechEngineError(
            f"Text has {len(text)} characters; the limit is {MAX_CHUNK_CHARS}."
        )


def _read_clip(wav_path: Path) -> AudioClip:
    """!@brief Read a WAV file the model wrote into an AudioClip.

    @param wav_path Path of the WAV file.
    @return The bytes of the file with its parameters.
    @throws SpeechEngineError If the file is missing, empty or not a WAV file.
    """
    try:
        data = wav_path.read_bytes()
    except OSError as error:
        raise SpeechEngineError(f"The model wrote no audio file: {error}") from error
    if not data:
        raise SpeechEngineError("The model wrote an empty audio file.")
    try:
        with wave.open(str(wav_path), "rb") as reader:
            return AudioClip(
                data=data,
                sample_rate=reader.getframerate(),
                channels=reader.getnchannels(),
                sample_width=reader.getsampwidth(),
            )
    except (wave.Error, EOFError) as error:
        raise SpeechEngineError(
            f"The model wrote an invalid WAV file: {error}"
        ) from error
