"""
Unified Universal Translation Engine for Bodo.
Coordinates rule-based parsing, pivot bridging to 100+ languages,
Hugging Face NLLB neural inference, and LLM adapters.
"""

from dataclasses import dataclass
from typing import Optional, Union
from bodonlp.translator.rule_based import RuleBasedTranslator
from bodonlp.translator.pivot import PivotTranslator
from bodonlp.translator.hf_adapter import HuggingFaceTranslator
from bodonlp.translator.llm_adapter import LLMTranslator
from bodonlp.phonetics import devanagari_to_latin, detect_script
from bodonlp.constants import Script


@dataclass
class TranslationResult:
    text: str                       # Translated output text
    romanized: str                  # Phonetic Latin transliteration (for Bodo)
    source: str                     # Original input string
    source_lang: str                # Source language code
    target_lang: str = "brx"        # Target language code
    method: str = "auto"            # "rule_based", "pivot", "hf", "llm", "web"
    confidence: float = 1.0

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<TranslationResult text='{self.text}' romanized='{self.romanized}' method='{self.method}'>"


class Translator:
    def __init__(self):
        self.rule_based = RuleBasedTranslator()
        self.pivot = PivotTranslator()
        self.hf = HuggingFaceTranslator()
        self.llm = LLMTranslator()

    def translate(
        self,
        text: str,
        source: str = "auto",
        target: str = "brx",
        method: str = "auto",
        api_key: Optional[str] = None
    ) -> TranslationResult:
        """
        Universal bidirectional translator for Bodo and world languages.
        
        Args:
            text: Text to translate.
            source: Source language code (e.g. 'en', 'hi', 'brx', 'fr', 'auto').
            target: Target language code (e.g. 'brx' for Bodo, 'en', 'hi', etc.).
            method: 'auto', 'rule_based', 'pivot', 'hf', or 'llm'.
            api_key: Optional Gemini or OpenAI API key.
        """
        clean_text = text.strip()
        if not clean_text:
            return TranslationResult(
                text="", romanized="", source=text,
                source_lang=source, target_lang=target,
                method="none", confidence=0.0
            )

        src = source.lower().strip()
        tgt = target.lower().strip()

        # Script / Language detection if auto
        if src in ("auto", ""):
            # Check if input text contains Devanagari
            has_dev = any(0x0900 <= ord(c) <= 0x097F for c in clean_text)
            if has_dev:
                # If target is English or other language, default source is Bodo (brx)
                if tgt in ("en", "eng", "english") or tgt != "brx":
                    src = "brx"
                else:
                    src = "hi"
            else:
                # Latin text. Check if first word is Bodo greeting / pronoun
                first_w = clean_text.split()[0].lower()
                if first_w in ("khulumbai", "mwjang", "ang", "nwng", "biyw", "jwng") or tgt in ("en", "eng"):
                    from bodonlp.lexicon.dictionary import get_lexicon
                    if get_lexicon().lookup(first_w):
                        src = "brx"
                    else:
                        src = "en"
                else:
                    src = "en"

        # Determine direction: Translating FROM Bodo or TO Bodo
        is_from_bodo = src in ("brx", "bodo", "brx_deva")

        # 1. LLM Translation if requested or if API key provided
        if method == "llm" or (api_key and method == "auto"):
            custom_llm = LLMTranslator(api_key=api_key) if api_key else self.llm
            if custom_llm.is_available():
                res = custom_llm.translate(clean_text, source_lang=src, target_lang=tgt)
                if res and res[0]:
                    dev, rom = res
                    return TranslationResult(
                        text=dev,
                        romanized=rom,
                        source=clean_text,
                        source_lang=src,
                        target_lang=tgt,
                        method="llm",
                        confidence=0.98
                    )

        # 2. Hugging Face Translation if method == 'hf'
        if method == "hf" and self.hf.is_available():
            src_nllb = "brx_Deva" if is_from_bodo else ("eng_Latn" if src == "en" else "hin_Deva")
            tgt_nllb = "eng_Latn" if tgt == "en" else "brx_Deva"
            res = self.hf.translate(clean_text, src_lang=src_nllb, tgt_lang=tgt_nllb)
            if res:
                return TranslationResult(
                    text=res,
                    romanized=devanagari_to_latin(res) if tgt in ("brx", "bodo") else "",
                    source=clean_text,
                    source_lang=src,
                    target_lang=tgt,
                    method="hf",
                    confidence=0.95
                )

        # 3. Translating FROM Bodo TO Other Languages
        if is_from_bodo:
            if tgt in ("en", "eng", "english"):
                out_en, conf = self.rule_based.translate_brx_to_en(clean_text)
                return TranslationResult(
                    text=out_en,
                    romanized="",
                    source=clean_text,
                    source_lang="brx",
                    target_lang="en",
                    method="rule_based",
                    confidence=conf
                )
            else:
                # Pivot to foreign target language (e.g., French, Spanish, Assamese)
                out_tgt, conf = self.pivot.translate_from_bodo(clean_text, target_lang=tgt)
                return TranslationResult(
                    text=out_tgt,
                    romanized="",
                    source=clean_text,
                    source_lang="brx",
                    target_lang=tgt,
                    method="pivot",
                    confidence=conf
                )

        # 4. Translating TO Bodo FROM English or Hindi
        if src in ("en", "eng", "english"):
            bodo_out, conf = self.rule_based.translate_en_to_brx(clean_text)
            return TranslationResult(
                text=bodo_out,
                romanized=devanagari_to_latin(bodo_out),
                source=clean_text,
                source_lang="en",
                target_lang="brx",
                method="rule_based",
                confidence=conf
            )
        elif src in ("hi", "hin", "hindi"):
            bodo_out, conf = self.rule_based.translate_en_to_brx(clean_text)
            return TranslationResult(
                text=bodo_out,
                romanized=devanagari_to_latin(bodo_out),
                source=clean_text,
                source_lang="hi",
                target_lang="brx",
                method="rule_based",
                confidence=conf
            )
        else:
            # 5. Translating TO Bodo from any other language via Pivot
            bodo_out, conf = self.pivot.translate_to_bodo(clean_text, source_lang=src)
            return TranslationResult(
                text=bodo_out,
                romanized=devanagari_to_latin(bodo_out),
                source=clean_text,
                source_lang=src,
                target_lang="brx",
                method="pivot",
                confidence=conf
            )


def translate(
    text: str,
    source: str = "auto",
    target: str = "brx",
    method: str = "auto",
    api_key: Optional[str] = None
) -> TranslationResult:
    """Convenience functional translation API."""
    translator = Translator()
    return translator.translate(text, source=source, target=target, method=method, api_key=api_key)
