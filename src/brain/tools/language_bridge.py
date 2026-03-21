"""
Multilingual support for CivicNerve.
Detects South African languages and normalizes input to English for the AI pipeline,
then translates responses back for citizens.

Supported: Zulu (zu), Sotho (st), Afrikaans (af), Xhosa (xh), English (en).
"""
from typing import Tuple

SA_LANGUAGES = {
    "zu": "Zulu",
    "st": "Sotho",
    "af": "Afrikaans",
    "xh": "Xhosa",
    "en": "English"
}


def normalize_to_english(text: str) -> Tuple[str, str]:
    """
    Detects the language of the input and translates to English if needed.
    Returns (english_text, detected_language_code).
    Falls back to treating input as English on any error.
    """
    try:
        from langdetect import detect
        lang = detect(text)
        if lang in SA_LANGUAGES and lang != "en":
            from deep_translator import GoogleTranslator
            translated = GoogleTranslator(source=lang, target="en").translate(text)
            return translated, lang
    except Exception:
        pass
    return text, "en"


def respond_in_language(text: str, target_lang: str) -> str:
    """Translates a response back into the citizen's language."""
    if not target_lang or target_lang == "en":
        return text
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except Exception:
        return text
