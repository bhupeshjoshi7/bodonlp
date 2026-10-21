"""
Bodo Syntax and Sentence Construction Engine.
Coordinates Subject-Object-Verb (SOV) structure, polar interrogatives, and echo words.
"""

from typing import Optional
from bodonlp.grammar.verb import conjugate
from bodonlp.grammar.noun import decline_noun
from bodonlp.constants import Case


def build_sentence(
    subject: str,
    object_: Optional[str] = None,
    verb: str = "जा",
    tense: str = "present",
    negative: bool = False,
    interrogative: bool = False,
    script: str = "devanagari"
) -> str:
    """
    Construct a grammatically well-formed Bodo sentence following canonical SOV word order.
    
    Args:
        subject: Subject in Bodo (e.g., 'आं', 'नों', 'बियो').
        object_: Optional direct or indirect object (e.g., 'ओंखाम', 'फरायसालि').
        verb: Verb root or infinitive (e.g., 'जा', 'थां', 'माव').
        tense: 'present', 'present_continuous', 'past', 'future', etc.
        negative: Negation flag.
        interrogative: Whether to form a question with interrogative particle -ना (-na).
        script: 'devanagari' or 'latin'.
        
    Examples:
        build_sentence("आं", "ओंखाम", "जा", "present") -> "आं ओंखाम जायो।"
        build_sentence("आं", "हाबा", "माव", "present_continuous") -> "आं हाबा मावदों।"
        build_sentence("बियो", "न'", "थां", "future") -> "बियो न' थांगोन।"
        build_sentence("नों", "ओंखाम", "जा", "past", interrogative=True) -> "नों ओंखाम जाबायना?"
    """
    is_rom = script.lower() in ("latin", "roman", "eng")
    
    subj_part = subject.strip()
    obj_part = object_.strip() if object_ else ""
    
    verb_form = conjugate(verb, tense=tense, negative=negative, script=script)
    
    components = [subj_part]
    if obj_part:
        components.append(obj_part)
        
    if interrogative:
        q_particle = "na?" if is_rom else "ना?"
        # In Bodo, polar question particle -ना cliticizes directly to the finite verb
        sentence = f"{' '.join(components)} {verb_form}{q_particle}"
    else:
        punct = "." if is_rom else "।"
        sentence = f"{' '.join(components)} {verb_form}{punct}"
        
    return sentence


def echo_word(word: str) -> str:
    """
    Form a Bodo expressive echo-word / reduplicated pair.
    Bodo widely uses echoic compounding to express generality or habit.
    
    Examples:
        echo_word("हाबा") -> "हाबा-हुखा" (work and chores)
        echo_word("जानाय") -> "जानाय-लोंनाय" (eating and drinking / feasts)
    """
    clean = word.strip()
    known_pairs = {
        "हाबा": "हाबा-हुखा",
        "जानाय": "जानाय-लोंनाय",
        "दै": "दै-दौ",
        "अं": "अं-एं",
        "लाइजाम": "लाइजाम-बिजाब",
        "haba": "haba-hukha",
        "janai": "janai-lwngnai",
    }
    if clean.lower() in known_pairs:
        return known_pairs[clean.lower()]
    return f"{clean}-{clean}"
