"""
Bodo phonetics, script detection, and bidirectional transliteration engine
between Devanagari (बर' हांखो) and Latin / Romanized scripts.
"""

import re
from typing import List, Tuple
from bodonlp.constants import Script


# Devanagari to Latin character and matra mappings tailored for Bodo phonetics
DEV_TO_LATIN = {
    # Vowels
    'अ': 'o', 'आ': 'a', 'इ': 'i', 'ई': 'i', 'उ': 'u', 'ऊ': 'u',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
    'अं': 'ong', 'अः': 'ah', 'ऑ': 'o',
    
    # Consonants
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
    'च': 's', 'छ': 's', 'ज': 'z', 'झ': 'zh', 'ञ': 'ny',
    'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'f', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'w',
    'श': 's', 'ष': 's', 'स': 's', 'ह': 'h',
    'ड़': 'r', 'ढ़': 'rh', 'य़': 'y',
    
    # Vowel signs (Matras)
    'ा': 'a', 'ि': 'i', 'ी': 'i', 'ु': 'u', 'ू': 'u',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
    '्': '', 'ं': 'ng', 'ः': 'h', 'ँ': 'n',
    'ऽ': "'", "’": "'", "‘": "'", "'": "'",
}

# Latin to Devanagari mapping for Bodo
LATIN_TO_DEV_VOWELS = {
    'ai': 'ऐ', 'au': 'औ', 'ng': 'ङ', 'kh': 'ख', 'gh': 'घ',
    'zh': 'झ', 'ny': 'ञ', 'th': 'थ', 'dh': 'ध', 'bh': 'भ',
    'sh': 'स', 'ch': 'च', 'a': 'आ', 'i': 'इ', 'u': 'उ',
    'e': 'ए', 'o': 'अ', 'w': 'व', 'y': 'य',
}

LATIN_TO_MATRAS = {
    'ai': 'ै', 'au': 'ौ', 'a': 'ा', 'i': 'ि', 'ee': 'ी',
    'u': 'ु', 'oo': 'ू', 'e': 'े', 'o': 'ो', 'w': '्व',
}

CONSONANTS_DEV = set('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहड़ढ़य़')
MATRAS_DEV = set('ािीुूेैोौ्ंःँऽ')


def normalize_devanagari(text: str) -> str:
    """Normalize common Unicode Devanagari variations and apostrophes in Bodo text."""
    if not text:
        return ""
    # Standardize Bodo high-tone apostrophe: बर' vs बर’ vs बर\'
    t = text.replace("’", "'").replace("‘", "'").replace("`", "'")
    # Normalize zero-width joiners
    t = t.replace("\u200c", "").replace("\u200d", "")
    # Normalize nukhta combinations
    t = t.replace("ड़", "र").replace("ढ़", "रह")
    return t.strip()


def detect_script(text: str) -> Script:
    """Detect whether input text is written in Devanagari or Latin script."""
    if not text:
        return Script.LATIN
    dev_count = sum(1 for c in text if 0x0900 <= ord(c) <= 0x097F)
    lat_count = sum(1 for c in text if (0x0041 <= ord(c) <= 0x005A) or (0x0061 <= ord(c) <= 0x007A))
    
    if dev_count >= lat_count and dev_count > 0:
        return Script.DEVANAGARI
    return Script.LATIN


def devanagari_to_latin(text: str) -> str:
    """
    Transliterate Bodo text in Devanagari into standard phonetic Latin script.
    Accurately accounts for Bodo inherent vowels, matras, and conjuncts.
    """
    if not text:
        return ""
    norm = normalize_devanagari(text)
    result = []
    i = 0
    n = len(norm)
    
    while i < n:
        ch = norm[i]
        
        # Check two-character compound (like अं)
        if i + 1 < n and norm[i:i+2] in DEV_TO_LATIN:
            result.append(DEV_TO_LATIN[norm[i:i+2]])
            i += 2
            continue
            
        if ch in CONSONANTS_DEV:
            next_ch = norm[i+1] if i + 1 < n else None
            base = DEV_TO_LATIN.get(ch, ch)
            
            if next_ch == '्':  # Halant (no vowel)
                result.append(base)
                i += 2
                continue
            elif next_ch in MATRAS_DEV:  # Explicit matra
                result.append(base)
                result.append(DEV_TO_LATIN.get(next_ch, ''))
                i += 2
                continue
            else:
                # Inherent vowel in Bodo is 'o' (or 'a' at end of words/particles)
                # At end of word, inherent vowel often drops or sounds as 'o'
                if next_ch is None or next_ch in ' \t\n.,!?;:()[]"\'':
                    result.append(base)
                else:
                    result.append(base + 'o')
                i += 1
                continue
                
        elif ch in DEV_TO_LATIN:
            result.append(DEV_TO_LATIN[ch])
            i += 1
        else:
            result.append(ch)
            i += 1
            
    res = ''.join(result)
    # Phonetic cleanups for common Bodo letter combinations
    res = re.sub(r'o([aeiou])', r'\1', res)
    res = re.sub(r'([bdfghjklmnprstvwz])o$', r'\1', res)  # terminal consonant suppression
    return res.strip()


def latin_to_devanagari(text: str) -> str:
    """
    Convert Romanized/Latin Bodo text into standard Devanagari script.
    Supports digraphs (kh, gh, ng, zh, ny, th, dh, bh, ai, au, etc.).
    """
    if not text:
        return ""
    
    # Pre-tokenization by words
    words = text.split()
    converted_words = []
    
    for word in words:
        clean_w = word.lower()
        res = []
        i = 0
        wlen = len(clean_w)
        
        # Check word-level direct exceptions or greetings
        if clean_w in ("khulumbai", "khulumbai!"):
            converted_words.append("खुलुमबाय")
            continue
        if clean_w == "mwjang":
            converted_words.append("मोजां")
            continue
        if clean_w == "ang":
            converted_words.append("आं")
            continue
        if clean_w == "nwng":
            converted_words.append("नों")
            continue
        if clean_w == "biyw":
            converted_words.append("बियो")
            continue
        if clean_w == "jwng":
            converted_words.append("जों")
            continue
        if clean_w == "biswr":
            converted_words.append("बिसोर")
            continue
            
        consonant_map = {
            'kh': 'ख', 'gh': 'घ', 'ng': 'ङ', 'zh': 'झ', 'ny': 'ञ',
            'th': 'थ', 'dh': 'ध', 'bh': 'भ', 'sh': 'स', 'ch': 'च',
            'ph': 'फ', 'k': 'क', 'g': 'ग', 's': 'स', 'z': 'ज',
            'j': 'ज', 't': 'त', 'd': 'द', 'n': 'न', 'p': 'प',
            'f': 'फ', 'b': 'ब', 'm': 'म', 'y': 'य', 'r': 'र',
            'l': 'ल', 'w': 'व', 'v': 'व', 'h': 'ह'
        }
        
        while i < wlen:
            # Check 2-letter consonants
            cand2 = clean_w[i:i+2]
            cand1 = clean_w[i]
            
            if cand2 in consonant_map:
                c_dev = consonant_map[cand2]
                i += 2
                # Check following vowel/matra
                if i < wlen:
                    v_cand2 = clean_w[i:i+2]
                    v_cand1 = clean_w[i]
                    if v_cand2 in LATIN_TO_MATRAS:
                        res.append(c_dev + LATIN_TO_MATRAS[v_cand2])
                        i += 2
                    elif v_cand1 in LATIN_TO_MATRAS:
                        res.append(c_dev + LATIN_TO_MATRAS[v_cand1])
                        i += 1
                    elif v_cand1 in ('w', 'o'):
                        res.append(c_dev + 'ो')
                        i += 1
                    else:
                        res.append(c_dev)
                else:
                    res.append(c_dev)
            elif cand1 in consonant_map:
                c_dev = consonant_map[cand1]
                i += 1
                if i < wlen:
                    v_cand2 = clean_w[i:i+2]
                    v_cand1 = clean_w[i]
                    if v_cand2 in LATIN_TO_MATRAS:
                        res.append(c_dev + LATIN_TO_MATRAS[v_cand2])
                        i += 2
                    elif v_cand1 in LATIN_TO_MATRAS:
                        res.append(c_dev + LATIN_TO_MATRAS[v_cand1])
                        i += 1
                    elif v_cand1 in ('w', 'o'):
                        res.append(c_dev + 'ो')
                        i += 1
                    else:
                        res.append(c_dev)
                else:
                    res.append(c_dev)
            elif cand2 in LATIN_TO_DEV_VOWELS:
                res.append(LATIN_TO_DEV_VOWELS[cand2])
                i += 2
            elif cand1 in LATIN_TO_DEV_VOWELS:
                res.append(LATIN_TO_DEV_VOWELS[cand1])
                i += 1
            else:
                res.append(clean_w[i])
                i += 1
                
        converted_words.append(''.join(res))
        
    return ' '.join(converted_words)


def tokenize(text: str) -> List[str]:
    """Tokenize Bodo text into words and punctuation marks."""
    if not text:
        return []
    return re.findall(r"[\u0900-\u097F\w']+|[^\s\w]", text, re.UNICODE)


def syllables(word: str) -> List[str]:
    """Break a Bodo word into constituent syllables."""
    if not word:
        return []
    clean = normalize_devanagari(word)
    # Split on vowel nuclei
    parts = []
    curr = []
    for ch in clean:
        curr.append(ch)
        if ch in MATRAS_DEV or ch in ('अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ'):
            parts.append(''.join(curr))
            curr = []
    if curr:
        if parts:
            parts[-1] += ''.join(curr)
        else:
            parts.append(''.join(curr))
    return parts if parts else [word]
