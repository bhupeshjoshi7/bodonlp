"""
Bodo Lexicon and Multi-Way Dictionary Engine.
Provides high-speed indexing and fuzzy searching across Bodo Devanagari, Romanized Bodo,
English, and Hindi.
"""

import json
import random
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

DATA_DIR = Path(__file__).resolve().parent / "data"

STOPWORDS_EN = {
    "a", "an", "the", "and", "or", "of", "in", "on", "at", "to", "for", "with", "by", "from",
    "is", "are", "was", "were", "be", "being", "been", "have", "has", "had", "do", "does", "did",
    "it", "its", "this", "that", "these", "those", "like", "such", "as", "about", "into", "through",
    "after", "before", "between", "under", "over", "above", "below", "some", "any", "which", "who",
    "whom", "whose", "where", "when", "why", "how", "all", "both", "each", "few", "more", "most",
    "other", "same", "so", "than", "too", "very", "can", "will", "just", "should", "now"
}

# English common synonym mappings to facilitate lookup
ENGLISH_SYNONYM_FALLBACKS: Dict[str, str] = {
    # Greetings & Common
    "hi": "hello", "hey": "hello", "namaste": "hello", "greetings": "hello",
    "bye": "goodbye", "bye-bye": "goodbye", "thanks": "thank you", "ty": "thank you",
    "yeah": "yes", "yep": "yes", "nope": "no", "nah": "no",
    
    # Kinship
    "mom": "mother", "mum": "mother", "mommy": "mother", "maa": "mother", "ma": "mother",
    "dad": "father", "daddy": "father", "papa": "father", "pa": "father",
    "bro": "brother", "sis": "sister", "grandpa": "grandfather", "grandma": "grandmother",
    "son": "son", "daughter": "daughter", "child": "child", "children": "child", "kid": "child",
    
    # Food & Drink
    "water": "water", "rice": "rice", "food": "food", "tea": "tea", "milk": "milk",
    "bread": "bread", "fish": "fish", "meat": "meat", "egg": "egg",
    
    # Animals & Nature
    "dog": "dog", "doggy": "dog", "puppy": "dog", "cat": "cat", "kitty": "cat",
    "cow": "cow", "cattle": "cow", "tiger": "tiger", "elephant": "elephant",
    "bird": "bird", "tree": "tree", "river": "river", "sun": "sun", "moon": "moon",
    "star": "star", "rain": "rain", "earth": "land", "land": "land", "house": "house", "home": "house",
}


@dataclass
class Word:
    bodo: str
    roman: str
    english: str
    hindi: str
    pos: str
    category: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __repr__(self) -> str:
        return f"Word(bodo='{self.bodo}', roman='{self.roman}', english='{self.english}', pos='{self.pos}', category='{self.category}')"


class Lexicon:
    _instance: Optional["Lexicon"] = None

    def __init__(self):
        self._words: List[Word] = []
        self._bodo_map: Dict[str, Word] = {}
        self._roman_map: Dict[str, Word] = {}
        self._english_exact_map: Dict[str, Word] = {}
        self._english_map: Dict[str, List[Word]] = {}
        self._hindi_exact_map: Dict[str, Word] = {}
        self._hindi_map: Dict[str, List[Word]] = {}
        self._phrases: List[Dict[str, Any]] = []
        self._proverbs: List[Dict[str, Any]] = []
        self._riddles: List[Dict[str, Any]] = []
        
        self._load_data()

    @classmethod
    def get_instance(cls) -> "Lexicon":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_data(self):
        # 1. Load words
        words_path = DATA_DIR / "words.json"
        if words_path.exists():
            with open(words_path, "r", encoding="utf-8") as f:
                raw_words = json.load(f)
                for item in raw_words:
                    word = Word(
                        bodo=item.get("bodo", "").strip(),
                        roman=item.get("roman", "").strip(),
                        english=item.get("english", "").strip(),
                        hindi=item.get("hindi", "").strip(),
                        pos=item.get("pos", "noun"),
                        category=item.get("category", "general"),
                    )
                    if not word.bodo and not word.english:
                        continue
                        
                    self._words.append(word)

                    # Bodo Devanagari indexing
                    if word.bodo and word.bodo not in self._bodo_map:
                        self._bodo_map[word.bodo] = word

                    # Romanized indexing
                    rom_key = word.roman.lower().strip()
                    if rom_key and rom_key not in self._roman_map:
                        self._roman_map[rom_key] = word

                    # English indexing
                    if word.english:
                        clean_en_raw = re.sub(r'[\(\)\[\]\{\}]', ' ', word.english.lower())
                        en_parts = [p.strip() for p in re.split(r'[,/;|\n]+', clean_en_raw) if p.strip()]
                        
                        for part in en_parts:
                            clean_part = re.sub(r'^[a-z]+\.\s*', '', part).strip()
                            if clean_part:
                                if clean_part not in self._english_exact_map:
                                    self._english_exact_map[clean_part] = word
                                spaced_part = re.sub(r'[-_]', ' ', clean_part).strip()
                                if spaced_part not in self._english_exact_map:
                                    self._english_exact_map[spaced_part] = word
                                    
                                self._english_map.setdefault(clean_part, []).append(word)
                                
                                for token in spaced_part.split():
                                    if token not in STOPWORDS_EN and len(token) > 1:
                                        self._english_map.setdefault(token, []).append(word)

                    # Hindi indexing
                    if word.hindi:
                        hi_clean = word.hindi.strip()
                        if hi_clean not in self._hindi_exact_map:
                            self._hindi_exact_map[hi_clean] = word
                        self._hindi_map.setdefault(hi_clean, []).append(word)

        # 2. Load phrases and index them into lookup maps
        phrases_path = DATA_DIR / "phrases.json"
        if phrases_path.exists():
            with open(phrases_path, "r", encoding="utf-8") as f:
                self._phrases = json.load(f)
                for p in self._phrases:
                    p_word = Word(
                        bodo=p.get("bodo", "").strip(),
                        roman=p.get("roman", "").strip(),
                        english=p.get("english", "").strip(),
                        hindi=p.get("hindi", "").strip(),
                        pos="phrase",
                        category=p.get("category", "phrases"),
                    )
                    if p_word.bodo not in self._bodo_map:
                        self._bodo_map[p_word.bodo] = p_word
                    if p_word.roman.lower() not in self._roman_map:
                        self._roman_map[p_word.roman.lower()] = p_word
                    en_clean = p_word.english.lower().strip()
                    if en_clean not in self._english_exact_map:
                        self._english_exact_map[en_clean] = p_word
                    self._words.append(p_word)

        # 3. Load proverbs
        proverbs_path = DATA_DIR / "proverbs.json"
        if proverbs_path.exists():
            with open(proverbs_path, "r", encoding="utf-8") as f:
                self._proverbs = json.load(f)

        # 4. Load riddles
        riddles_path = DATA_DIR / "riddles.json"
        if riddles_path.exists():
            with open(riddles_path, "r", encoding="utf-8") as f:
                self._riddles = json.load(f)

    def total_words(self) -> int:
        """Return total number of loaded vocabulary entries."""
        return len(self._words)

    def lookup(self, term: str) -> Optional[Word]:
        """
        Look up a term across Bodo Devanagari, Romanized Bodo, English, or Hindi.
        Returns the best matching Word object, or None if not found.
        """
        clean = term.strip()
        if not clean:
            return None

        # 1. Exact Bodo Devanagari match
        if clean in self._bodo_map:
            return self._bodo_map[clean]

        # 2. Normalized Devanagari (handle apostrophes)
        clean_dev = clean.replace("’", "'").replace("‘", "'")
        if clean_dev in self._bodo_map:
            return self._bodo_map[clean_dev]

        # 3. Exact Romanized match
        clean_rom = clean.lower()
        if clean_rom in self._roman_map:
            return self._roman_map[clean_rom]

        # 4. English Exact Match
        if clean_rom in self._english_exact_map:
            return self._english_exact_map[clean_rom]

        # 5. English Synonym Fallback
        if clean_rom in ENGLISH_SYNONYM_FALLBACKS:
            canonical = ENGLISH_SYNONYM_FALLBACKS[clean_rom]
            if canonical in self._english_exact_map:
                return self._english_exact_map[canonical]

        # 6. Hindi Match
        if clean in self._hindi_exact_map:
            return self._hindi_exact_map[clean]

        # 7. Substring or token match in English map
        if clean_rom in self._english_map and len(self._english_map[clean_rom]) > 0:
            return self._english_map[clean_rom][0]

        return None

    def search(self, query: str, limit: int = 10) -> List[Word]:
        """
        Perform a fuzzy/prefix search across all fields in the dictionary.
        """
        q = query.strip().lower()
        if not q:
            return []

        results = []
        seen = set()

        # Direct exact match first
        exact = self.lookup(query)
        if exact:
            results.append(exact)
            seen.add(exact.bodo)

        for w in self._words:
            if len(results) >= limit:
                break
            if w.bodo in seen:
                continue
                
            # Check matches
            if (q in w.bodo.lower() or
                q in w.roman.lower() or
                q in w.english.lower() or
                (w.hindi and q in w.hindi)):
                results.append(w)
                seen.add(w.bodo)

        return results

    def get_phrases(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return conversational phrases, optionally filtered by category."""
        if not category:
            return self._phrases
        c = category.lower().strip()
        return [p for p in self._phrases if p.get("category", "").lower() == c]

    def get_proverbs(self) -> List[Dict[str, Any]]:
        """Return all traditional Bodo proverbs (फाथास)."""
        return self._proverbs

    def random_proverb(self) -> Optional[Dict[str, Any]]:
        """Return a random Bodo proverb."""
        return random.choice(self._proverbs) if self._proverbs else None

    def get_riddles(self) -> List[Dict[str, Any]]:
        """Return all traditional Bodo riddles (खानथि / सोल')."""
        return self._riddles

    def random_riddle(self) -> Optional[Dict[str, Any]]:
        """Return a random Bodo riddle."""
        return random.choice(self._riddles) if self._riddles else None


def get_lexicon() -> Lexicon:
    """Get the singleton Lexicon instance."""
    return Lexicon.get_instance()


def lookup(term: str) -> Optional[Word]:
    """Look up a word across Bodo, Romanized, English, or Hindi."""
    return get_lexicon().lookup(term)


def search(query: str, limit: int = 10) -> List[Word]:
    """Search for words matching a query."""
    return get_lexicon().search(query, limit=limit)
