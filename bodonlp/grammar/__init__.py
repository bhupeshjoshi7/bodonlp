"""
Bodo Grammar and Morphology Package.
"""

from bodonlp.grammar.noun import (
    pluralize,
    decline_noun,
    attach_case_marker,
)
from bodonlp.grammar.verb import (
    conjugate,
    extract_root,
    COMMON_VERBS,
)
from bodonlp.grammar.pronouns import (
    get_pronoun,
    PRONOUN_TABLE,
    DEMONSTRATIVES,
    INTERROGATIVES,
    PronounForms,
)
from bodonlp.grammar.syntax import (
    build_sentence,
    echo_word,
)

__all__ = [
    "pluralize",
    "decline_noun",
    "attach_case_marker",
    "conjugate",
    "extract_root",
    "COMMON_VERBS",
    "get_pronoun",
    "PRONOUN_TABLE",
    "DEMONSTRATIVES",
    "INTERROGATIVES",
    "PronounForms",
    "build_sentence",
    "echo_word",
]
