"""
Bodo Verb Morphology & Conjugation Engine.
Handles tense inflection, aspect, negation, imperative, and participial forms.
"""

from typing import Dict, Optional, Tuple
from bodonlp.constants import Tense


# High-frequency Bodo verb roots
COMMON_VERBS = {
    "eat": {"root_dev": "जा", "root_rom": "ja"},
    "go": {"root_dev": "थां", "root_rom": "thang"},
    "come": {"root_dev": "फै", "root_rom": "fwi"},
    "do": {"root_dev": "माव", "root_rom": "mao"},
    "work": {"root_dev": "माव", "root_rom": "mao"},
    "drink": {"root_dev": "लों", "root_rom": "lwng"},
    "speak": {"root_dev": "बुं", "root_rom": "bung"},
    "say": {"root_dev": "बुं", "root_rom": "bung"},
    "see": {"root_dev": "नु", "root_rom": "nu"},
    "look": {"root_dev": "नाय", "root_rom": "nai"},
    "read": {"root_dev": "फराय", "root_rom": "forai"},
    "write": {"root_dev": "लिर", "root_rom": "lir"},
    "know": {"root_dev": "रों", "root_rom": "rwng"},
    "learn": {"root_dev": "सोलों", "root_rom": "swlwng"},
    "sleep": {"root_dev": "उन्दु", "root_rom": "undu"},
    "give": {"root_dev": "हो", "root_rom": "ho"},
    "take": {"root_dev": "ला", "root_rom": "la"},
    "buy": {"root_dev": "बाय", "root_rom": "bai"},
    "sell": {"root_dev": "फान", "root_rom": "fan"},
    "run": {"root_dev": "खार", "root_rom": "khar"},
    "sing": {"root_dev": "रोजाब", "root_rom": "rozab"},
    "dance": {"root_dev": "मोसा", "root_rom": "mosa"},
    "laugh": {"root_dev": "मिनि", "root_rom": "mini"},
    "cry": {"root_dev": "गाब", "root_rom": "gab"},
    "live": {"root_dev": "था", "root_rom": "tha"},
    "stay": {"root_dev": "था", "root_rom": "tha"},
    "die": {"root_dev": "थै", "root_rom": "thwi"},
}


def extract_root(verb: str) -> str:
    """Extract base verbal root by removing common inflectional suffixes."""
    v = verb.strip()
    for suffix in ("दोंमोन", "थागोन", "नाय", "दों", "बाय", "गोन", "मोन", "यो", "दो", "आ"):
        if v.endswith(suffix) and len(v) > len(suffix):
            return v[:-len(suffix)]
    return v


def conjugate(
    verb: str,
    tense: str = "present",
    negative: bool = False,
    script: str = "devanagari"
) -> str:
    """
    Conjugate a Bodo verb according to tense, aspect, and polarity.
    
    Args:
        verb: Root verb in Devanagari or English meaning (e.g., 'जा', 'थां', 'eat', 'go').
        tense: 'present', 'present_continuous', 'past', 'past_continuous', 'future', 'imperative'.
        negative: If True, returns negated form.
        script: 'devanagari' or 'latin'.
        
    Examples:
        conjugate("जा", "present") -> "जायो"
        conjugate("जा", "present_continuous") -> "जादों"
        conjugate("जा", "past") -> "जाबाय"
        conjugate("जा", "future") -> "जागोन"
        conjugate("जा", "present", negative=True) -> "जाया"
        conjugate("थां", "future", negative=True) -> "थाङा"
    """
    is_rom = script.lower() in ("latin", "roman", "eng")
    clean_v = verb.strip()
    
    # Resolve English verb to root
    if clean_v.lower() in COMMON_VERBS:
        v_info = COMMON_VERBS[clean_v.lower()]
        root = v_info["root_rom"] if is_rom else v_info["root_dev"]
    else:
        root = extract_root(clean_v)
        
    t = tense.lower()
    
    # Handle Negation
    if negative:
        if is_rom:
            if t == "imperative":
                return f"da-{root}"
            # Negation suffix -a or -ya
            suf = "ya" if root.endswith(('a', 'i', 'u', 'e', 'o')) else "a"
            return f"{root}{suf}"
        else:
            if t == "imperative":
                return f"दा{root}"
            # Bodo negation: root + -या (vowel root) or -आ (consonant root)
            if root.endswith(('ा', 'ि', 'ी', 'ु', 'ू', 'े', 'ै', 'ो', 'ौ', 'आ', 'इ', 'उ', 'ए', 'ओ')):
                return f"{root}या"
            elif root.endswith('ं'):
                return f"{root[:-1]}ङा"
            else:
                return f"{root}आ"

    # Positive conjugation
    if is_rom:
        if t in ("present", "indefinite"):
            suf = "yo" if root.endswith(('a', 'i', 'u', 'e', 'o')) else "o"
            return f"{root}{suf}"
        elif t in ("present_continuous", "continuous"):
            return f"{root}dwng"
        elif t in ("past", "perfect"):
            return f"{root}bai"
        elif t in ("past_continuous",):
            return f"{root}dwngmwn"
        elif t in ("future",):
            return f"{root}-gwn"
        elif t in ("imperative",):
            return f"{root}do"
        elif t in ("verbal_noun", "gerund", "infinitive"):
            return f"{root}nai"
        return root
    else:
        if t in ("present", "indefinite"):
            if root.endswith(('ा', 'ि', 'ी', 'ु', 'ू', 'े', 'ै', 'ो', 'ौ', 'आ', 'इ', 'उ', 'ए', 'ओ')):
                return f"{root}यो"
            elif root.endswith('ं'):
                return f"{root[:-1]}ङो"
            else:
                return f"{root}ओ"
        elif t in ("present_continuous", "continuous"):
            return f"{root}दों"
        elif t in ("past", "perfect"):
            return f"{root}बाय"
        elif t in ("past_continuous",):
            return f"{root}दोंमोन"
        elif t in ("future",):
            return f"{root}गोन"
        elif t in ("imperative",):
            return f"{root}दो"
        elif t in ("verbal_noun", "gerund", "infinitive"):
            return f"{root}नाय"
        return root
