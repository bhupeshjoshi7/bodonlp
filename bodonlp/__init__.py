"""
Bodo (बड़ो / बर') Language Standard Library for Python
======================================================

A comprehensive, standard-library-style NLP and linguistic toolkit for the Bodo language
(ISO 639-3: `brx`, FLORES/NLLB: `brx_Deva`), providing:
- 36,000+ entry multi-way dictionary lookup (Bodo, Romanized, English, Hindi)
- Universal bidirectional translation (Bodo <-> 100+ World Languages)
- Rich morphology, SOV syntax engine, case declension, and verb conjugation
- Unique Bodo numeral classifier system (सा-, मा-, गं-, दं-, थाइ-)
- Phonetics, script detection, and Devanagari <-> Romanized transliteration
- Speech synthesis cadence, tone profiling, and SSML generator
- Cultural heritage engine: festivals, musical instruments, attire, clans, and Bathou tradition
- Internet scrapers for Bodo Wikipedia, Wikimedia Incubator, Glosbe, and corpus mining

Quick Start:
------------
>>> import bodonlp
>>> bodonlp.translate("Hello, how are you?")
<TranslationResult text='मा खबर?' romanized='Ma khobor?' method='rule_based'>
>>> bodonlp.translate("आं मोजाङैनो दं", target="en")
<TranslationResult text='I am fine' romanized='' method='rule_based'>
>>> bodonlp.lookup("खुलुमबाय")
Word(bodo='खुलुमबाय', roman='Khulumbai', english='Hello / Greetings', pos='interjection', category='greetings')
>>> bodonlp.conjugate("जा", tense="past")
'जाबाय'
>>> bodonlp.num_to_words(42)
'ब्रैजिनै'
>>> bodonlp.numbers.apply_classifier("mansi", 2)
'सानै मानसि'
>>> bodonlp.transliterate("Khulumbai", to_script="devanagari")
'खुलुमबाय'
"""

__version__ = "1.0.0"
__author__ = "Bhupesh Joshi"
__email__ = "bhupeshjoshi@example.com"
__license__ = "MIT"

# Constants
from bodonlp.constants import (
    ISO_639_3,
    ISO_639_NAME,
    ISO_639_1,
    NATIVE_NAME,
    NATIVE_NAME_ALT,
    NLLB_CODE,
    FLORES_CODE,
    Script,
    Dialect,
    PartOfSpeech,
    Tense,
    Case,
    CASE_MARKERS,
    NUMERAL_CLASSIFIERS,
    KINSHIP,
    SEASONS,
    BODO_MONTHS,
    DAYS_OF_WEEK,
    BODO_CLANS,
)

# Phonetics & Transliteration
from bodonlp.phonetics import (
    normalize_devanagari as normalize,
    detect_script,
    devanagari_to_latin,
    latin_to_devanagari,
    tokenize,
    syllables,
)

# Number System
from bodonlp.numbers import (
    num_to_words,
    words_to_num,
    to_devanagari_numerals,
    from_devanagari_numerals,
    ordinal,
    fraction,
    apply_classifier,
    get_classifier_for,
    list_classifiers,
)

# Grammar & Morphology
from bodonlp.grammar import (
    pluralize,
    decline_noun,
    attach_case_marker,
    conjugate,
    extract_root,
    get_pronoun,
    PRONOUN_TABLE,
    DEMONSTRATIVES,
    INTERROGATIVES,
    build_sentence,
    echo_word,
    COMMON_VERBS,
)

# Lexicon & Dictionary
from bodonlp.lexicon import (
    Word,
    Lexicon,
    get_lexicon,
    lookup,
    search,
)

# Translation Engine
from bodonlp.translator import (
    Translator,
    TranslationResult,
    translate,
    RuleBasedTranslator,
    PivotTranslator,
    HuggingFaceTranslator,
    LLMTranslator,
    WebTranslator,
)

# Subpackages
from bodonlp import numbers
from bodonlp import grammar
from bodonlp import lexicon
from bodonlp import translator
from bodonlp import culture
from bodonlp import scraper
from bodonlp import voice


def transliterate(text: str, to_script: str = "devanagari") -> str:
    """
    Universal transliterator between Latin and Devanagari scripts for Bodo.
    
    Args:
        text: Input string in either Latin or Devanagari.
        to_script: Target script ('devanagari' or 'latin' / 'roman').
    """
    to_s = to_script.lower()
    if to_s in ("devanagari", "dev", "brx"):
        return latin_to_devanagari(text)
    elif to_s in ("latin", "roman", "eng"):
        return devanagari_to_latin(text)
    return text


# Cultural facade helpers
def get_proverbs():
    """Return all traditional Bodo proverbs (फाथास / Bathra Sao)."""
    return get_lexicon().get_proverbs()


def random_proverb():
    """Return a random Bodo proverb."""
    return get_lexicon().random_proverb()


def get_riddles():
    """Return all traditional Bodo riddles (खानथि / Sol)."""
    return get_lexicon().get_riddles()


def random_riddle():
    """Return a random Bodo riddle."""
    return get_lexicon().random_riddle()


def get_phrases(category: str = None):
    """Return curated conversational Bodo phrases."""
    return get_lexicon().get_phrases(category=category)


__all__ = [
    # Metadata
    "__version__",
    "__author__",
    "ISO_639_3",
    "ISO_639_NAME",
    "NATIVE_NAME",
    "NATIVE_NAME_ALT",
    "NLLB_CODE",
    # Phonetics
    "normalize",
    "detect_script",
    "devanagari_to_latin",
    "latin_to_devanagari",
    "transliterate",
    "tokenize",
    "syllables",
    # Numbers
    "num_to_words",
    "words_to_num",
    "to_devanagari_numerals",
    "from_devanagari_numerals",
    "ordinal",
    "fraction",
    "apply_classifier",
    # Grammar
    "pluralize",
    "decline_noun",
    "attach_case_marker",
    "conjugate",
    "extract_root",
    "get_pronoun",
    "build_sentence",
    "echo_word",
    # Lexicon
    "Word",
    "Lexicon",
    "get_lexicon",
    "lookup",
    "search",
    "get_proverbs",
    "random_proverb",
    "get_riddles",
    "random_riddle",
    "get_phrases",
    # Translation
    "Translator",
    "TranslationResult",
    "translate",
    # Submodules
    "numbers",
    "grammar",
    "lexicon",
    "translator",
    "culture",
    "scraper",
    "voice",
]
