"""
Bodo Voice and Speech Synthesis Helper Package.
Provides phonetic cadence, syllable stress, SSML generation, and speech translation bridging.
"""

from dataclasses import dataclass
from typing import List, Optional
from bodonlp.translator.engine import Translator
from bodonlp.voice.cadence import generate_cadence, to_ssml, detect_tone
from bodonlp.phonetics import devanagari_to_latin, syllables


@dataclass
class VoiceTranslationResult:
    source_text: str
    source_lang: str
    translated_text: str            # Bodo Devanagari
    romanized: str                  # Phonetic Latin
    syllables: List[str]            # Constituent syllables
    ssml: str                       # Formatted SSML markup
    tone_profile: str


class VoiceTranslator:
    def __init__(self):
        self.translator = Translator()

    def translate_for_voice(
        self,
        text: str,
        source_lang: str = "auto",
        rate: str = "medium"
    ) -> VoiceTranslationResult:
        """
        Translate input text to Bodo and prepare acoustic phonetic annotations and SSML.
        """
        trans_res = self.translator.translate(text, source=source_lang, target="brx")
        bodo_text = trans_res.text
        rom = trans_res.romanized or devanagari_to_latin(bodo_text)
        
        all_syls = []
        for word in bodo_text.split():
            all_syls.extend(syllables(word))
            
        ssml_markup = to_ssml(bodo_text, rate=rate)
        has_high_tone = any(detect_tone(w) == "high_pitch" for w in bodo_text.split())
        tone_profile = "high_tone_present" if has_high_tone else "standard_pitch"
        
        return VoiceTranslationResult(
            source_text=text,
            source_lang=trans_res.source_lang,
            translated_text=bodo_text,
            romanized=rom,
            syllables=all_syls,
            ssml=ssml_markup,
            tone_profile=tone_profile
        )


def voice_translate(text: str, source_lang: str = "auto") -> VoiceTranslationResult:
    """Convenience helper for voice-ready translation."""
    vt = VoiceTranslator()
    return vt.translate_for_voice(text, source_lang=source_lang)


__all__ = [
    "VoiceTranslator",
    "VoiceTranslationResult",
    "voice_translate",
    "generate_cadence",
    "to_ssml",
    "detect_tone",
]
