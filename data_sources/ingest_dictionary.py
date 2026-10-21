"""
Pipeline to clean, normalize, and ingest dictionary data from Bihung (Bodo Sahitya Sabha)
into bodonlp standard lexicon format.
"""

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRATCH_DIR = Path(r"C:\Users\Bhupesh\.gemini\antigravity-ide\brain\c0b2bc68-c0c1-4434-a835-fb02a0c3a877\scratch")
BIHUNG_DATA = SCRATCH_DIR / "bihung" / "data.json"
OUTPUT_DIR = ROOT_DIR / "bodonlp" / "lexicon" / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Transliteration mapping table for Bodo Devanagari to Latin
DEV_TO_LATIN = {
    'अ': 'o', 'आ': 'a', 'इ': 'i', 'ई': 'i', 'उ': 'u', 'ऊ': 'u',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au', 'अं': 'ong', 'अः': 'ah',
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
    'च': 's', 'छ': 's', 'ज': 'z', 'झ': 'zh', 'ञ': 'ny',
    'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'f', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'w',
    'श': 's', 'ष': 's', 'स': 's', 'ह': 'h',
    'ड़': 'r', 'ढ़': 'rh', 'य़': 'y',
    'ा': 'a', 'ि': 'i', 'ी': 'i', 'ु': 'u', 'ू': 'u',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', '्': '',
    'ं': 'ng', 'ः': 'h', 'ँ': 'n', 'ऽ': "'",
}

def devanagari_to_roman(text: str) -> str:
    """Accurate transliteration of Bodo Devanagari text to Romanized script."""
    if not text:
        return ""
    result = []
    i = 0
    n = len(text)
    
    consonants = set('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहड़ढ़य़')
    matras = set('ािीुूेैोौ्ंःँऽ')
    
    while i < n:
        ch = text[i]
        if ch in consonants:
            # Check next character
            next_ch = text[i+1] if i + 1 < n else None
            trans = DEV_TO_LATIN.get(ch, ch)
            if next_ch == '्':
                result.append(trans)
                i += 2
                continue
            elif next_ch in matras:
                result.append(trans)
                i += 1
                continue
            else:
                # Default inherent vowel in Bodo is often 'o' or 'a' depending on position; 'o'/'a'
                result.append(trans + 'o')
                i += 1
                continue
        elif ch in DEV_TO_LATIN:
            result.append(DEV_TO_LATIN[ch])
            i += 1
        else:
            result.append(ch)
            i += 1
            
    res = ''.join(result)
    # Clean up double vowels and trailing markers
    res = re.sub(r'o([aeiou])', r'\1', res)
    return res.strip()

def detect_pos(bodo_def: list, eng_def: list) -> str:
    combined = ' '.join(bodo_def + eng_def)
    if 'बि.' in combined or 'noun' in combined.lower():
        return 'noun'
    elif 'दि.' in combined or 'verb' in combined.lower() or any(e.startswith('to ') for e in eng_def):
        return 'verb'
    elif 'म.' in combined or 'adj' in combined.lower():
        return 'adjective'
    elif 'थ.' in combined or 'adv' in combined.lower():
        return 'adverb'
    elif 'pronoun' in combined.lower():
        return 'pronoun'
    return 'noun'

def main():
    print(f"Reading {BIHUNG_DATA}...")
    with open(BIHUNG_DATA, 'r', encoding='utf-8') as f:
        bihung = json.load(f)
        
    raw_words = bihung.get('words', [])
    processed_words = []
    seen = set()

    # Domain mapping
    domain_map = {
        'dictionary': 'general',
        'archeology': 'archeology',
        'geology': 'geology',
        'fundamental adminstrative': 'administration',
        'computer science': 'technology',
        'sociology': 'culture',
        'education': 'education',
        'farming': 'agriculture',
        'geography': 'geography',
    }

    for item in raw_words:
        headword = item.get('word', '').strip()
        b_list = item.get('b', [])
        e_list = item.get('e', [])
        source = item.get('s', 'dictionary').lower().strip()
        category = domain_map.get(source, 'general')
        
        if not headword:
            continue
            
        has_dev = any(0x0900 <= ord(c) <= 0x097F for c in headword)
        
        if has_dev:
            # Bodo headword
            bodo_text = headword
            eng_gloss = '; '.join([e.strip() for e in e_list if e.strip()])
            if not eng_gloss and b_list:
                # Bodo definition
                bodo_gloss = '; '.join([b.strip() for b in b_list if b.strip()])
                eng_gloss = bodo_gloss
            pos = detect_pos(b_list, e_list)
            roman = devanagari_to_roman(bodo_text)
            
            key = (bodo_text, eng_gloss.lower())
            if key in seen:
                continue
            seen.add(key)
            
            processed_words.append({
                "bodo": bodo_text,
                "roman": roman,
                "english": eng_gloss,
                "hindi": "",
                "pos": pos,
                "category": category
            })
        else:
            # English headword -> Bodo translation in b_list
            eng_text = headword
            for bodo_cand in b_list:
                clean_bodo = bodo_cand.strip()
                if not clean_bodo:
                    continue
                roman = devanagari_to_roman(clean_bodo)
                key = (clean_bodo, eng_text.lower())
                if key in seen:
                    continue
                seen.add(key)
                
                processed_words.append({
                    "bodo": clean_bodo,
                    "roman": roman,
                    "english": eng_text,
                    "hindi": "",
                    "pos": "noun",
                    "category": category
                })

    print(f"Total processed dictionary entries: {len(processed_words)}")
    
    out_file = OUTPUT_DIR / "words.json"
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(processed_words, f, ensure_ascii=False, indent=2)
    print(f"Saved {out_file} successfully! Size: {out_file.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
