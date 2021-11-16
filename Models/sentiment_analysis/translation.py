import typing as t
import time

from googletrans import Translator


def detect_swedish_manually(text: str) -> t.Optional[str]:
    """Get language if text is Swedish."""
    return 'sv' if any(char in text.lower() for char in {'å', 'ä', 'ö'}) else None


def get_detected_lang(text: str) -> t.Optional[str]:
    """Use Google Translate API to detect language."""
    translator = Translator()
    try:
        time.sleep(0.5)
        return translator.detect(text).lang
    except Exception as e:
        # (Probably) invoked API rate limit
        # Google translation allows for 5 calls/s and maximum 200k per day.
        raise e


def get_language(text: str, lang_detection_status: bool) -> t.Tuple[t.Optional[str], bool]:
    """Get detected language and language detection status."""
    if lang_detection_status:
        try:
            return get_detected_lang(text), True
        except Exception:
            # Continue to use manual fallback function.
            pass
    return detect_swedish_manually(text), False
