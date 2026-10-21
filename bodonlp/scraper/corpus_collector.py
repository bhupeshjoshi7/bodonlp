"""
Corpus Collector & Processor for Bodo Language.
Aggregates, cleans, and standardizes Bodo text corpora from web and dataset sources.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set, Optional
from bodonlp.phonetics import normalize_devanagari


class CorpusCollector:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "bodo_corpus"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def clean_text(self, text: str) -> str:
        """Clean raw scraped text: strip HTML, normalize whitespace, standardize punctuation."""
        t = re.sub(r'<[^>]+>', ' ', text)
        t = re.sub(r'http[s]?://\S+', '', t)
        t = normalize_devanagari(t)
        t = re.sub(r'\s+', ' ', t)
        return t.strip()

    def extract_sentences(self, text: str) -> List[str]:
        """Split Bodo text into discrete sentences using Devanagari danda and standard punctuation."""
        clean = self.clean_text(text)
        if not clean:
            return []
        sentences = re.split(r'[।!?\n]+', clean)
        return [s.strip() for s in sentences if len(s.strip()) > 3]

    def build_vocabulary(self, sentences: List[str]) -> Dict[str, int]:
        """Compute word frequency distribution for Bodo text."""
        freq: Dict[str, int] = {}
        for s in sentences:
            tokens = re.findall(r"[\u0900-\u097F']+", s)
            for t in tokens:
                if len(t) > 1:
                    freq[t] = freq.get(t, 0) + 1
        return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

    def save_corpus_file(self, filename: str, sentences: List[str]):
        """Save clean sentence corpus to text file."""
        target = self.output_dir / filename
        with open(target, "w", encoding="utf-8") as f:
            for s in sentences:
                f.write(s + "।\n")
        print(f"Saved {len(sentences)} sentences to {target}")
