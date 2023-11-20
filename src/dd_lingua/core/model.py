from lingua import DetectionResult, Language, LanguageDetectorBuilder
from loguru import logger

from dd_lingua.core.utils import (DEFAULT_LANGUAGES, LinguaSupportedISO639_3,
                                  LinguaSupportedISO15924,
                                  map_iso639_to_langcode)


class Lingua:
    """Lingua model wrapper"""

    def __init__(
        self,
        eager_mode: bool = False,
        script: LinguaSupportedISO15924 = None,
        languages: list[LinguaSupportedISO639_3] = None,
        low_accuracy: bool = True,
    ):
        if languages:
            logger.debug(f"Using languages: {languages}")
            languages = [map_iso639_to_langcode(iso) for iso in languages]
            _builder = LanguageDetectorBuilder.from_iso_codes_639_3(*languages)
        elif script:
            logger.debug(f"Using all languages for script {script}")
            _builder = self.map_script_to_build(script)
        elif eager_mode:
            logger.debug("Using eager mode for all non-extint languages")
            _builder = LanguageDetectorBuilder.from_all_spoken_languages()
        else:
            logger.debug(f"Using default languages: {DEFAULT_LANGUAGES}")
            languages = [map_iso639_to_langcode(iso) for iso in DEFAULT_LANGUAGES]
            _builder = LanguageDetectorBuilder.from_iso_codes_639_3(*languages)

        if low_accuracy:
            logger.debug("Using low accuracy mode")
            _builder = _builder.with_low_accuracy_mode()

        self._model = _builder.build()

    @staticmethod
    def map_script_to_build(script: LinguaSupportedISO15924):
        if script == LinguaSupportedISO15924.Arab:
            return LanguageDetectorBuilder.from_all_arabic_languages()
        elif script == LinguaSupportedISO15924.Cyrl:
            return LanguageDetectorBuilder.from_all_cyrillic_languages()
        elif script == LinguaSupportedISO15924.Deva:
            return LanguageDetectorBuilder.from_all_devanagari_languages()
        elif script == LinguaSupportedISO15924.Latn:
            return LanguageDetectorBuilder.from_all_latin_languages()
        else:
            raise ValueError(f"Script {script} not supported")

    @staticmethod
    def standardize_lang(lang: Language):
        return {"language": lang.iso_code_639_3.name.lower()}

    @staticmethod
    def standardize_detection(det: DetectionResult):
        return {
            **Lingua.standardize_lang(det.language),
            "offset": det.start_index,
            "length": det.end_index - det.start_index,
        }

    def infer(self, text: str, multilingual: bool = False, max_chars: int = 5_000):
        """Predict the language of a text

        Args:
            text (str): Text to predict
            multilingual (bool): Whether to detect mmultiple languages (ie. code-switching). Defaults to False.
            max_characters (int): Maximum number of characters to use for prediction. Defaults to 5_000.

        """
        text = text[:max_chars]

        if multilingual:
            return [Lingua.standardize_detection(detection) for detection in self._model.detect_multiple_languages_of(text)]
        return Lingua.standardize_lang(self._model.detect_language_of(text))
