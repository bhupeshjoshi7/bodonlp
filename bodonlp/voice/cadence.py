"""
Bodo Phonetic Cadence, Tone Analysis, and SSML Generation for Speech Synthesis.
Bodo features a distinct two-tone phonological pitch contrast (High Tone vs Low Tone).
"""

from typing import List, Dict, Any, Tuple
import re
from bodonlp.phonetics import syllables, devanagari_to_latin, normalize_devanagari


def detect_tone(word: str) -> str:
    """
    Detect tonal pitch contour in a Bodo word.
    In written Bodo, high tone is often marked by an apostrophe (') or specific vowel combinations.
    """
    clean = normalize_devanagari(word)
    if "'" in clean or "’" in clean or "‘" in clean:
        return "high_pitch"
    # Lexical high tone indicators
    if any(clean.startswith(prefix) for prefix in ("बर'", "गथ'", "न'", "द'")):
        return "high_pitch"
    return "low_pitch"


def generate_cadence(text: str) -> Dict[str, Any]:
    """
    Analyze the spoken cadence of a Bodo sentence or phrase,
    producing syllable breakdown, tone profiling, and phonetic flow.
    """
    words = text.split()
    word_cadences = []
    
    for w in words:
        syls = syllables(w)
        tone = detect_tone(w)
        rom = devanagari_to_latin(w)
        word_cadences.append({
            "word": w,
            "roman": rom,
            "syllables": syls,
            "syllable_count": len(syls),
            "tone": tone
        })
        
    return {
        "text": text,
        "romanized": devanagari_to_latin(text),
        "words": word_cadences,
        "total_syllables": sum(wc["syllable_count"] for wc in word_cadences)
    }


def to_ssml(text: str, rate: str = "medium", pitch: str = "medium") -> str:
    """
    Convert Bodo text into Speech Synthesis Markup Language (SSML)
    with prosody controls and pauses tailored for Bodo phonetics.
    """
    cadence = generate_cadence(text)
    ssml_parts = [f'<speak><prosody rate="{rate}" pitch="{pitch}">']
    
    for wc in cadence["words"]:
        w = wc["word"]
        tone = wc["tone"]
        if tone == "high_pitch":
            ssml_parts.append(f'<prosody pitch="+5%">{w}</prosody>')
        else:
            ssml_parts.append(w)
            
    ssml_parts.append('</prosody></speak>')
    return " ".join(ssml_parts)
