"""
Bodo Universal Translation Package.
"""

from bodonlp.translator.engine import (
    Translator,
    TranslationResult,
    translate,
)
from bodonlp.translator.rule_based import RuleBasedTranslator
from bodonlp.translator.pivot import PivotTranslator
from bodonlp.translator.hf_adapter import HuggingFaceTranslator
from bodonlp.translator.llm_adapter import LLMTranslator
from bodonlp.translator.web_adapter import WebTranslator

__all__ = [
    "Translator",
    "TranslationResult",
    "translate",
    "RuleBasedTranslator",
    "PivotTranslator",
    "HuggingFaceTranslator",
    "LLMTranslator",
    "WebTranslator",
]
