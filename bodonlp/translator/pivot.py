"""
Universal Pivot Translation Engine.
Bridges Bodo to and from 100+ global languages using English or Hindi as an intermediate pivot.
"""

from typing import Tuple, Optional
from bodonlp.translator.rule_based import RuleBasedTranslator


class PivotTranslator:
    def __init__(self):
        self.rule_based = RuleBasedTranslator()

    def translate_to_bodo(
        self,
        text: str,
        source_lang: str = "es"
    ) -> Tuple[str, float]:
        """
        Translate foreign language text into Bodo via English pivot.
        
        Args:
            text: Input text in source foreign language (e.g., 'Bonjour', 'Hola', 'Assamese').
            source_lang: ISO 639-1 code of source language.
        """
        clean = text.strip()
        if not clean:
            return "", 0.0

        # Try using deep_translator if installed
        pivot_english = None
        try:
            from deep_translator import GoogleTranslator
            pivot_english = GoogleTranslator(source=source_lang, target="en").translate(clean)
        except Exception:
            # Basic fallback for common global greetings
            global_greetings = {
                "bonjour": "hello", "hola": "hello", "ciao": "hello",
                "hallo": "hello", "namaste": "hello", "konnichiwa": "hello",
                "merci": "thank you", "gracias": "thank you", "danke": "thank you",
                "arigato": "thank you", "adios": "goodbye", "au revoir": "goodbye"
            }
            pivot_english = global_greetings.get(clean.lower(), clean)

        if not pivot_english:
            pivot_english = clean

        # Translate English to Bodo
        bodo_text, conf = self.rule_based.translate_en_to_brx(pivot_english)
        return bodo_text, conf * 0.9

    def translate_from_bodo(
        self,
        bodo_text: str,
        target_lang: str = "fr"
    ) -> Tuple[str, float]:
        """
        Translate Bodo text into target foreign language via English pivot.
        
        Args:
            bodo_text: Text in Bodo Devanagari or Romanized script.
            target_lang: ISO 639-1 target language code (e.g., 'fr', 'es', 'de', 'ja', 'as').
        """
        clean = bodo_text.strip()
        if not clean:
            return "", 0.0

        # Translate Bodo to English first
        en_text, conf = self.rule_based.translate_brx_to_en(clean)

        # Translate English to Target Language
        try:
            from deep_translator import GoogleTranslator
            res = GoogleTranslator(source="en", target=target_lang).translate(en_text)
            return res, conf * 0.95
        except Exception:
            return en_text, conf * 0.7
