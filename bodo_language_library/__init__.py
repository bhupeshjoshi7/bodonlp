"""
Bodo Language Library (bodo_language_library)
=============================================

A comprehensive standard-library-style NLP and linguistic toolkit for the Bodo language
(बड़ो / बर', ISO 639-3: brx, FLORES/NLLB: brx_Deva).

Quick Start:
------------
>>> import bodo_language_library as bodo
>>> bodo.translate("Hello, how are you?")
<TranslationResult text='मा खबर?' romanized='Ma khobor?' method='rule_based'>
>>> bodo.lookup("खुलुमबाय")
Word(bodo='खुलुमबाय', roman='Khulumbai', english='Hello / Greetings', ...)
"""

import bodonlp
from bodonlp import *
from bodonlp import (
    numbers,
    grammar,
    lexicon,
    translator,
    culture,
    scraper,
    voice,
    constants,
    phonetics,
    cli,
)

__version__ = bodonlp.__version__
__author__ = bodonlp.__author__
__all__ = bodonlp.__all__
