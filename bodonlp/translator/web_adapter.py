"""
Free Web Translation Adapter.
Provides fallback translation using open web translation APIs.
"""

import json
import urllib.request
import urllib.parse
from typing import Optional, Tuple


class WebTranslator:
    def __init__(self):
        pass

    def translate_to_english(self, text: str, source_lang: str = "auto") -> Optional[str]:
        """Translate any language to English via free web API."""
        try:
            url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={source_lang}|en"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                if data.get("responseStatus") == 200:
                    return data.get("responseData", {}).get("translatedText")
        except Exception:
            pass
        return None

    def translate_from_english(self, text: str, target_lang: str = "fr") -> Optional[str]:
        """Translate English to any target language via free web API."""
        try:
            url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=en|{target_lang}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                if data.get("responseStatus") == 200:
                    return data.get("responseData", {}).get("translatedText")
        except Exception:
            pass
        return None
