"""
Rule-Based Offline Translation Engine for Bodo.
Translates bidirectionally between English, Hindi, and Bodo using lexical lookup,
grammatical morpheme decomposition, and Subject-Object-Verb (SOV) reordering.
"""

import re
from typing import Tuple, Optional, List
from bodonlp.lexicon.dictionary import get_lexicon
from bodonlp.grammar.verb import conjugate, COMMON_VERBS, extract_root
from bodonlp.grammar.noun import decline_noun, pluralize
from bodonlp.grammar.pronouns import get_pronoun, DEMONSTRATIVES, INTERROGATIVES
from bodonlp.constants import Case
from bodonlp.phonetics import devanagari_to_latin


# Exact conversational translation pairs
EXACT_PHRASE_PAIRS = {
    # English to Bodo
    "hello": ("खुलुमबाय", "Khulumbai"),
    "hi": ("खुलुमबाय", "Khulumbai"),
    "greetings": ("खुलुमबाय", "Khulumbai"),
    "namaste": ("खुलुमबाय", "Khulumbai"),
    "good morning": ("गोजोन फुंबिलि", "Gwjwn fungbili"),
    "good evening": ("गोजोन बेलासै", "Gwjwn belase"),
    "good night": ("गोजोन हर", "Gwjwn hor"),
    "good day": ("गोजोन सान", "Gwjwn saan"),
    "how are you": ("मा खबर?", "Ma khobor?"),
    "how are you?": ("मा खबर?", "Ma khobor?"),
    "i am fine": ("आं मोजाङैनो दं", "Ang mwjangwinw dwng"),
    "i am good": ("आं मोजाङैनो दं", "Ang mwjangwinw dwng"),
    "i am well": ("आं मोजाङैनो दं", "Ang mwjangwinw dwng"),
    "what is your name": ("नोंनि मुंआ मा?", "Nwngni munga ma?"),
    "what is your name?": ("नोंनि मुंआ मा?", "Nwngni munga ma?"),
    "my name is": ("आंनि मुंआ", "Angni munga"),
    "thank you": ("गोजोन्थों", "Gwjwnthwng"),
    "thanks": ("गोजोन्थों", "Gwjwnthwng"),
    "goodbye": ("थाबाय दे", "Thabai de"),
    "bye": ("थाबाय दे", "Thabai de"),
    "see you": ("थाबाय दे", "Thabai de"),
    "sorry": ("निमाहा बिनो थाबाय", "Nimaha binw thabai"),
    "excuse me": ("निमाहा बिनो थाबाय", "Nimaha binw thabai"),
    "where are you going": ("नों बबेयाव थांगोन?", "Nwng bwbeyao thang-gwn?"),
    "where are you going?": ("नों बबेयाव थांगोन?", "Nwng bwbeyao thang-gwn?"),
    "i love you": ("आं नोंखौ मोजां मोनो", "Ang nwngkhou mwjang mwnw"),
    "welcome": ("बरायबाय", "Boraibai"),
    "yes": ("औ", "Ou"),
    "no": ("नङा", "Nonga"),
    "water": ("दै", "Dwi"),
    "food": ("ओंखाम", "Wngkham"),
    "rice": ("ओंखाम", "Wngkham"),
    
    # Hindi to Bodo
    "नमस्ते": ("खुलुमबाय", "Khulumbai"),
    "नमस्कार": ("खुलुमबाय", "Khulumbai"),
    "क्या हाल है": ("मा खबर?", "Ma khobor?"),
    "क्या हाल है?": ("मा खबर?", "Ma khobor?"),
    "मैं ठीक हूँ": ("आं मोजाङैनो दं", "Ang mwjangwinw dwng"),
    "आपका नाम क्या है": ("नोंनि मुंआ मा?", "Nwngni munga ma?"),
    "आपका नाम क्या है?": ("नोंनि मुंआ मा?", "Nwngni munga ma?"),
    "धन्यवाद": ("गोजोन्थों", "Gwjwnthwng"),
    "शुक्रिया": ("गोजोन्थों", "Gwjwnthwng"),
    "अलविदा": ("थाबाय दे", "Thabai de"),
    "माफ़ कीजिये": ("निमाहा बिनो थाबाय", "Nimaha binw thabai"),
    "हाँ": ("औ", "Ou"),
    "नहीं": ("नङा", "Nonga"),
    "पानी": ("दै", "Dwi"),
    "खाना": ("ओंखाम", "Wngkham"),
}

# Reverse exact pairs (Bodo to English)
BODO_TO_EN_EXACT = {
    "खुलुमबाय": "Hello / Greetings",
    "मा खबर?": "How are you?",
    "मा खबर": "How are you?",
    "मोजां": "Good / Fine",
    "आं मोजाङैनो दं": "I am fine",
    "नोंनि मुंआ मा?": "What is your name?",
    "नोंनि मुंआ मा": "What is your name?",
    "गोजोन्थों": "Thank you",
    "साबायखर": "Thank you",
    "थाबाय दे": "Goodbye",
    "गोजोन फुंबिलि": "Good morning",
    "गोजोन हर": "Good night",
    "औ": "Yes",
    "नङा": "No",
    "दै": "Water",
    "ओंखाम": "Rice / Food",
}


class RuleBasedTranslator:
    def __init__(self):
        self.lexicon = get_lexicon()

    def translate_en_to_brx(self, text: str) -> Tuple[str, float]:
        """
        Translate English text into Bodo Devanagari.
        Returns: (translated_bodo_text, confidence_score)
        """
        clean = text.strip()
        lower = clean.lower()

        # 1. Exact phrase lookup
        stripped_punct = re.sub(r'[?.!,;:]', '', lower).strip()
        if lower in EXACT_PHRASE_PAIRS:
            return EXACT_PHRASE_PAIRS[lower][0], 1.0
        if stripped_punct in EXACT_PHRASE_PAIRS:
            return EXACT_PHRASE_PAIRS[stripped_punct][0], 1.0

        # 2. Pronoun & SVO to SOV pattern matching
        # Examples: "I eat rice" -> "आं ओंखाम जायो"
        # "He is going to school" -> "बियो फरायसालियाव थांदों"
        tokens = [t.lower() for t in re.findall(r"\w+|[^\w\s]", clean) if t.strip()]
        
        # Check simple pattern: Subject + Verb + Object
        subject_map = {
            "i": "आं", "we": "जों", "you": "नों", "he": "बियो", "she": "बियो",
            "they": "बिसोर", "this": "बे", "that": "बै",
        }
        
        # Check if starts with known subject pronoun
        if len(tokens) >= 2 and tokens[0] in subject_map:
            subj_bodo = subject_map[tokens[0]]
            rest_tokens = tokens[1:]
            
            # Check for negative: "do not" / "does not" / "cannot"
            is_negative = False
            if len(rest_tokens) >= 2 and rest_tokens[0] in ("do", "does", "did") and rest_tokens[1] == "not":
                is_negative = True
                rest_tokens = rest_tokens[2:]
            elif len(rest_tokens) >= 1 and rest_tokens[0] in ("don't", "doesn't", "didn't"):
                is_negative = True
                rest_tokens = rest_tokens[1:]
                
            # Check for continuous: "am/is/are" + V-ing
            is_continuous = False
            if len(rest_tokens) >= 2 and rest_tokens[0] in ("am", "is", "are", "was", "were"):
                if rest_tokens[1].endswith("ing"):
                    is_continuous = True
                    verb_candidate = rest_tokens[1][:-3]
                    obj_tokens = rest_tokens[2:]
                else:
                    verb_candidate = None
                    obj_tokens = rest_tokens[1:]
            else:
                verb_candidate = rest_tokens[-1] if rest_tokens else None
                obj_tokens = rest_tokens[:-1] if len(rest_tokens) > 1 else []
                
            # Resolve verb
            verb_bodo = None
            if verb_candidate:
                for base_v, info in COMMON_VERBS.items():
                    if verb_candidate.startswith(base_v) or base_v.startswith(verb_candidate):
                        verb_bodo = info["root_dev"]
                        break
                if not verb_bodo:
                    w = self.lexicon.lookup(verb_candidate)
                    if w:
                        verb_bodo = w.bodo
                        
            # Resolve object
            obj_bodo_parts = []
            for tok in obj_tokens:
                if tok in ("to", "the", "a", "an", "at", "in"):
                    continue
                w = self.lexicon.lookup(tok)
                if w:
                    obj_bodo_parts.append(w.bodo)
                else:
                    obj_bodo_parts.append(tok)
                    
            if verb_bodo:
                tense = "present_continuous" if is_continuous else "present"
                v_finite = conjugate(verb_bodo, tense=tense, negative=is_negative)
                sentence_parts = [subj_bodo] + obj_bodo_parts + [v_finite]
                return " ".join(sentence_parts), 0.85

        # 3. Direct Word-by-word with grammatical classification
        bodo_tokens = []
        translated_count = 0
        total_tokens = len(tokens)
        
        for tok in tokens:
            if tok in ("the", "a", "an", "is", "are", "am"):
                continue
            w = self.lexicon.lookup(tok)
            if w:
                bodo_tokens.append(w.bodo)
                translated_count += 1
            else:
                bodo_tokens.append(tok)

        confidence = translated_count / max(1, total_tokens)
        return " ".join(bodo_tokens), round(confidence, 2)

    def translate_brx_to_en(self, text: str) -> Tuple[str, float]:
        """
        Translate Bodo text (Devanagari or Romanized) into English.
        Returns: (translated_english_text, confidence_score)
        """
        clean = text.strip()
        lower = clean.lower()

        # 1. Exact phrase matching
        if clean in BODO_TO_EN_EXACT:
            return BODO_TO_EN_EXACT[clean], 1.0
        stripped = clean.rstrip("?।!.,")
        if stripped in BODO_TO_EN_EXACT:
            return BODO_TO_EN_EXACT[stripped], 1.0

        # 2. Token decomposition
        tokens = clean.split()
        en_parts = []
        translated = 0

        for tok in tokens:
            w = self.lexicon.lookup(tok)
            if w and w.english:
                # Pick first English meaning
                primary = re.split(r'[,/;|\n]+', w.english)[0].strip()
                en_parts.append(primary)
                translated += 1
            else:
                # Try stripping common Bodo case suffixes (-खौ, -जों, -नो, -नि, -आव, -फोर)
                stemmed = None
                for suf in ("फोर", "खौ", "जों", "नो", "निफ्राय", "नि", "आव", "याव", "दों", "बाय", "गोन"):
                    if tok.endswith(suf) and len(tok) > len(suf):
                        cand = tok[:-len(suf)]
                        w_cand = self.lexicon.lookup(cand)
                        if w_cand and w_cand.english:
                            stemmed = re.split(r'[,/;|\n]+', w_cand.english)[0].strip()
                            break
                if stemmed:
                    en_parts.append(stemmed)
                    translated += 1
                else:
                    en_parts.append(tok)

        conf = translated / max(1, len(tokens))
        return " ".join(en_parts), round(conf, 2)
