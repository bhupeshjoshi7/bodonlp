"""
Bodo Pronoun Paradigm & Table.
Covers personal, demonstrative, and interrogative pronouns across all case declensions.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PronounForms:
    person: int                    # 1, 2, 3
    number: str                    # "singular" or "plural"
    nominative: str                # Subject (I / You / He)
    accusative: str                # Object (Me / You / Him)
    dative: str                    # Recipient (To me / To you)
    genitive: str                  # Possessive (My / Your / His)
    instrumental: str              # Comitative (With me / With you)
    locative: str                  # Locative (At/on me)
    roman_nom: str
    roman_gen: str


PRONOUN_TABLE: Dict[str, PronounForms] = {
    # 1st Person Singular
    "1s": PronounForms(
        person=1, number="singular",
        nominative="आं", accusative="आंखौ", dative="आंनो",
        genitive="आंनि", instrumental="आंजों", locative="आंनाव",
        roman_nom="ang", roman_gen="angni"
    ),
    # 1st Person Plural
    "1p": PronounForms(
        person=1, number="plural",
        nominative="जों", accusative="जोंखौ", dative="जोंनो",
        genitive="जोंनि", instrumental="जोंजों", locative="जोंनाव",
        roman_nom="jwng", roman_gen="jwngni"
    ),
    # 2nd Person Singular
    "2s": PronounForms(
        person=2, number="singular",
        nominative="नों", accusative="नोंखौ", dative="नोंनो",
        genitive="नोंनि", instrumental="नोंजों", locative="नोंनाव",
        roman_nom="nwng", roman_gen="nwngni"
    ),
    # 2nd Person Plural
    "2p": PronounForms(
        person=2, number="plural",
        nominative="नोंसोर", accusative="नोंसोरखौ", dative="नोंसोरनो",
        genitive="नोंसोरनि", instrumental="नोंसोरजों", locative="नोंसोरनाव",
        roman_nom="nwngswr", roman_gen="nwngswrni"
    ),
    # 3rd Person Singular
    "3s": PronounForms(
        person=3, number="singular",
        nominative="बियो", accusative="बिखौ", dative="बिनो",
        genitive="बिनि", instrumental="बिजों", locative="बिनाव",
        roman_nom="biyw", roman_gen="bini"
    ),
    # 3rd Person Plural
    "3p": PronounForms(
        person=3, number="plural",
        nominative="बिसोर", accusative="बिसोरखौ", dative="बिसोरनो",
        genitive="बिसोरनि", instrumental="बिसोरजों", locative="बिसोरनाव",
        roman_nom="biswr", roman_gen="biswrni"
    ),
}

# Demonstratives
DEMONSTRATIVES = {
    "this": {"dev": "बे", "rom": "be"},
    "that": {"dev": "बै", "rom": "bwi"},
    "these": {"dev": "बेफोर", "rom": "befur"},
    "those": {"dev": "बैफोर", "rom": "bwifur"},
}

# Interrogatives
INTERROGATIVES = {
    "who": {"dev": "सोर", "rom": "swr"},
    "whom": {"dev": "सोरखौ", "rom": "swrkhwo"},
    "whose": {"dev": "सोरनि", "rom": "swrni"},
    "what": {"dev": "मा", "rom": "ma"},
    "which": {"dev": "बबे", "rom": "bwbe"},
    "where": {"dev": "बबेयाव", "rom": "bwbeyao"},
    "when": {"dev": "माला", "rom": "mala"},
    "why": {"dev": "मानो", "rom": "manw"},
    "how": {"dev": "माबोरै", "rom": "maborwi"},
}


def get_pronoun(person: int = 1, plural: bool = False, case: str = "nom") -> str:
    """
    Get the Bodo pronoun form.
    
    Args:
        person: 1, 2, or 3.
        plural: True for plural, False for singular.
        case: 'nom', 'acc', 'dat', 'gen', 'inst', 'loc'.
    """
    key = f"{person}{'p' if plural else 's'}"
    forms = PRONOUN_TABLE.get(key, PRONOUN_TABLE["1s"])
    c = case.lower()
    if c in ("nom", "nominative", "subj"):
        return forms.nominative
    elif c in ("acc", "accusative", "obj"):
        return forms.accusative
    elif c in ("dat", "dative", "to"):
        return forms.dative
    elif c in ("gen", "genitive", "possessive"):
        return forms.genitive
    elif c in ("inst", "instrumental", "with"):
        return forms.instrumental
    elif c in ("loc", "locative"):
        return forms.locative
    return forms.nominative
