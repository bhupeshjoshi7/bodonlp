"""
Bodo Numeral Classifiers Engine.
In Bodo, numerals do not attach directly to nouns in isolation; they are prefixed or suffixed
with distinct categorical classifiers (e.g., सा- for humans, मा- for animals, गं- for flat/rigid objects).
"""

from typing import Dict, List, Optional, Tuple
from bodonlp.constants import NUMERAL_CLASSIFIERS


# High-frequency noun to classifier mapping
NOUN_CLASSIFIER_MAP: Dict[str, str] = {
    # Human beings (सा- / sa)
    "मानसि": "sa", "mansi": "sa", "person": "sa", "man": "sa",
    "फिसा": "sa", "fisa": "sa", "child": "sa", "kid": "sa",
    "गथ'": "sa", "gotho": "sa", "boy": "sa", "girl": "sa",
    "हौवा": "sa", "howa": "sa", "husband": "sa",
    "हिनजाव": "sa", "hinjao": "sa", "woman": "sa", "wife": "sa",
    "आफा": "sa", "afa": "sa", "father": "sa",
    "आइ": "sa", "aai": "sa", "mother": "sa",
    "फिसाला": "sa", "fisala": "sa", "son": "sa",
    "फिसाजो": "sa", "fisajw": "sa", "daughter": "sa",
    "लौगो": "sa", "lwgw": "sa", "friend": "sa",
    "फोरोंगिरि": "sa", "foronggiri": "sa", "teacher": "sa",
    "फरायसुला": "sa", "foraisula": "sa", "student": "sa",
    
    # Animals, birds, reptiles, insects (मा- / ma)
    "सैमा": "ma", "swima": "ma", "dog": "ma",
    "मावजि": "ma", "maoji": "ma", "cat": "ma",
    "म्वसौ": "ma", "mwswo": "ma", "cow": "ma", "cattle": "ma",
    "मोसा": "ma", "mosa": "ma", "tiger": "ma",
    "हाथि": "ma", "hathi": "ma", "elephant": "ma",
    "दाव": "ma", "dao": "ma", "bird": "ma", "chicken": "ma",
    "ना": "ma", "na": "ma", "fish": "ma",
    "जुनार": "ma", "junar": "ma", "animal": "ma",
    "एमफौ": "ma", "emfou": "ma", "insect": "ma",
    "जिबो": "ma", "jibo": "ma", "snake": "ma",
    "बोरमा": "ma", "borma": "ma", "goat": "ma",
    "अमा": "ma", "oma": "ma", "pig": "ma",
    "दावदै": "ma", "daodwi": "ma", "egg": "ma",
    
    # Flat, rigid, curved objects, utensils, tools, houses (गं- / gwng)
    "न'": "gwng", "no": "gwng", "house": "gwng", "room": "gwng",
    "थाला": "gwng", "thala": "gwng", "plate": "gwng",
    "बाथि": "gwng", "bathi": "gwng", "bowl": "gwng",
    "गेदा": "gwng", "geda": "gwng", "cup": "gwng",
    "दखना": "gwng", "dokhona": "gwng", "dress": "gwng",
    "आरोनाइ": "gwng", "aronai": "gwng", "scarf": "gwng",
    "गामसा": "gwng", "gamcha": "gwng", "towel": "gwng",
    "सिफुं": "gwng", "sifung": "gwng", "flute": "gwng",
    "खाम": "gwng", "kham": "gwng", "drum": "gwng",
    "सियार": "gwng", "chair": "gwng", "टेबल": "gwng", "table": "gwng",
    "लामा": "gwng", "lama": "gwng", "road": "gwng",
    
    # Long, cylindrical objects, tall flora, ropes, rivers (दं- / dwng)
    "बिफां": "dwng", "bifang": "dwng", "tree": "dwng", "plant": "dwng",
    "दैसा": "dwng", "dwisa": "dwng", "river": "dwng", "stream": "dwng",
    "दुलि": "dwng", "duli": "dwng", "rope": "dwng", "string": "dwng",
    "लावथि": "dwng", "laothi": "dwng", "stick": "dwng", "cane": "dwng",
    "पेन्सिल": "dwng", "pencil": "dwng", "कलम": "dwng", "pen": "dwng",
    "खामफा": "dwng", "pillar": "dwng", "post": "dwng",
    
    # Fruits, spherical, seeds, round objects (थाइ- / thai)
    "फिथाइ": "thai", "fithai": "thai", "fruit": "thai",
    "थाइजौ": "thai", "thaijou": "thai", "mango": "thai",
    "थाख्रि": "thai", "thakhri": "thai", "banana": "thai",
    "कसु": "thai", "kosu": "thai", "taro": "thai",
    "ग'म": "thai", "gom": "thai", "potato": "thai",
    "टमाटर": "thai", "tomato": "thai",
    
    # Leaves, thin flat sheets (बिसि- / bisi)
    "बिलाइ": "bisi", "bilai": "bisi", "leaf": "bisi", "sheet": "bisi", "page": "bisi",
    "लेखा": "bisi", "lekha": "bisi", "paper": "bisi",
    
    # Books, layers, volumes (खोलोब- / kholob)
    "बिजाब": "kholob", "bijab": "kholob", "book": "kholob",
    "लाइजाम": "kholob", "laijam": "kholob", "letter": "kholob",
}

# Number roots for classifier attachment
NUM_ROOTS_DEV = {
    1: "से", 2: "नै", 3: "थाम", 4: "ब्रै", 5: "बा",
    6: "द'", 7: "स्नि", 8: "दाइन", 9: "गु", 10: "जि"
}

NUM_ROOTS_ROM = {
    1: "se", 2: "nwi", 3: "tham", 4: "brwi", 5: "ba",
    6: "do", 7: "sni", 8: "daen", 9: "gu", 10: "zi"
}


def get_classifier_for(noun: str) -> Optional[str]:
    """Retrieve the classifier key for a given noun."""
    clean = noun.lower().strip()
    return NOUN_CLASSIFIER_MAP.get(clean)


def apply_classifier(noun: str, count: int, script: str = "devanagari") -> str:
    """
    Apply appropriate Bodo classifier to a noun and numeral count.
    
    Example:
        apply_classifier("मानसि", 1) -> "सासे मानसि"
        apply_classifier("सैमा", 2) -> "मासे नै सैमा" / "मानै सैमा"
        apply_classifier("बिफां", 1) -> "दंसे बिफां"
        apply_classifier("थाइजौ", 3) -> "थाइथाम थाइजौ"
    """
    cls_key = get_classifier_for(noun) or "gwng"
    cls_info = NUMERAL_CLASSIFIERS.get(cls_key, NUMERAL_CLASSIFIERS["gwng"])
    
    marker_dev = cls_info["marker"]
    marker_rom = cls_info["roman"]
    
    if count in NUM_ROOTS_DEV:
        num_dev = NUM_ROOTS_DEV[count]
        num_rom = NUM_ROOTS_ROM[count]
        classified_dev = f"{marker_dev}{num_dev} {noun}"
        classified_rom = f"{marker_rom}{num_rom} {noun}"
    else:
        from bodonlp.numbers import num_to_words
        w_dev = num_to_words(count, "devanagari")
        w_rom = num_to_words(count, "latin")
        classified_dev = f"{marker_dev} {w_dev} {noun}"
        classified_rom = f"{marker_rom} {w_rom} {noun}"
        
    return classified_dev if script.lower().startswith("dev") else classified_rom


def list_classifiers() -> Dict[str, Dict[str, any]]:
    """Return all Bodo numeral classifiers with descriptions and examples."""
    return NUMERAL_CLASSIFIERS
