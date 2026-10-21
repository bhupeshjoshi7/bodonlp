"""
Bodo Noun Morphology: Pluralization, Case Declension, and Postpositions.
"""

from typing import Dict, Optional
from bodonlp.constants import Case, CASE_MARKERS


def pluralize(noun: str, script: str = "devanagari") -> str:
    """
    Pluralize a Bodo noun using the standard suffix -फोर (-fur / -phor).
    
    Examples:
        pluralize("मानसि") -> "मानसिफोर"
        pluralize("सैमा") -> "सैमाफोर"
        pluralize("mansi", script="latin") -> "mansifur"
    """
    clean = noun.strip()
    is_rom = script.lower() in ("latin", "roman", "eng")
    suffix = "fur" if is_rom else "फोर"
    return f"{clean}{suffix}"


def decline_noun(noun: str, case: Case, script: str = "devanagari") -> str:
    """
    Decline a Bodo noun in a specific grammatical case.
    
    Cases:
        - Nominative: Subject (unmarked or -आ)
        - Accusative: -खौ (-khwo)
        - Instrumental: -जों (-jwng)
        - Dative: -नो (-nw)
        - Ablative: -निफ्राय (-nifrai)
        - Genitive: -नि (-ni)
        - Locative: -आव (-ao) / -याव (-yao)
    
    Examples:
        decline_noun("मानसि", Case.ACCUSATIVE) -> "मानसिखौ"
        decline_noun("न'", Case.LOCATIVE) -> "न'आव"
        decline_noun("हाजो", Case.ABLATIVE) -> "हाजोनिफ्राय"
    """
    clean = noun.strip()
    is_rom = script.lower() in ("latin", "roman", "eng")
    
    # Suffixes
    dev_suffixes = {
        Case.NOMINATIVE: "",
        Case.ACCUSATIVE: "खौ",
        Case.INSTRUMENTAL: "जों",
        Case.DATIVE: "नो",
        Case.ABLATIVE: "निफ्राय",
        Case.GENITIVE: "नि",
        Case.LOCATIVE: "आव",
    }
    
    rom_suffixes = {
        Case.NOMINATIVE: "",
        Case.ACCUSATIVE: "khwo",
        Case.INSTRUMENTAL: "jwng",
        Case.DATIVE: "nw",
        Case.ABLATIVE: "nifrai",
        Case.GENITIVE: "ni",
        Case.LOCATIVE: "ao",
    }
    
    suffixes = rom_suffixes if is_rom else dev_suffixes
    suf = suffixes.get(case, "")
    
    # Locative morphophonemic adjustment: if noun ends with vowel 'i' / 'e', add -याव (-yao)
    if case == Case.LOCATIVE and not is_rom:
        if clean.endswith(('ि', 'ी', 'े', 'ै')):
            suf = "याव"
            
    return f"{clean}{suf}"


def attach_case_marker(noun: str, marker_name: str) -> str:
    """Convenience helper to attach a named case marker."""
    m = marker_name.lower().strip()
    case_map = {
        "acc": Case.ACCUSATIVE, "accusative": Case.ACCUSATIVE,
        "inst": Case.INSTRUMENTAL, "instrumental": Case.INSTRUMENTAL,
        "dat": Case.DATIVE, "dative": Case.DATIVE,
        "abl": Case.ABLATIVE, "ablative": Case.ABLATIVE,
        "gen": Case.GENITIVE, "genitive": Case.GENITIVE, "possessive": Case.GENITIVE,
        "loc": Case.LOCATIVE, "locative": Case.LOCATIVE,
        "nom": Case.NOMINATIVE, "nominative": Case.NOMINATIVE,
    }
    c = case_map.get(m, Case.NOMINATIVE)
    return decline_noun(noun, c)
