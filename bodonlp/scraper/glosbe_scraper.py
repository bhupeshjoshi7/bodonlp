"""
Glosbe Bodo-English Bilingual Dictionary and Sentence Pair Scraper.
Fetches crowd-sourced translations and bilingual usage examples.
"""

import json
import re
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional


class GlosbeScraper:
    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"):
        self.base_url = "https://glosbe.com"
        self.user_agent = user_agent

    def fetch_translations(self, word: str, from_lang: str = "en", to_lang: str = "brx") -> List[str]:
        """
        Scrape translation options for a word from Glosbe.
        
        Args:
            word: Headword to query.
            from_lang: 'en' or 'brx'
            to_lang: 'brx' or 'en'
        """
        clean = word.strip()
        encoded = urllib.parse.quote(clean)
        url = f"{self.base_url}/{from_lang}/{to_lang}/{encoded}"
        
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        translations = []
        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                html = response.read().decode("utf-8", errors="ignore")
                # Parse translation phrases from HTML markup
                matches = re.findall(r'<h3 class="[^"]*translation[^"]*">([^<]+)</h3>', html)
                if not matches:
                    matches = re.findall(r'data-translation="([^"]+)"', html)
                translations = [m.strip() for m in matches if m.strip()]
        except Exception:
            pass
            
        return translations

    def fetch_sentence_pairs(self, word: str) -> List[Dict[str, str]]:
        """Scrape bilingual sentence pairs containing the word."""
        url = f"{self.base_url}/en/brx/{urllib.parse.quote(word)}"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        pairs = []
        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                html = response.read().decode("utf-8", errors="ignore")
                # Look for sentence blocks
                blocks = re.findall(r'<div class="[^"]*sentence-pair[^"]*">(.*?)</div>', html, re.DOTALL)
                for b in blocks:
                    texts = re.findall(r'<span[^>]*>([^<]+)</span>', b)
                    if len(texts) >= 2:
                        pairs.append({"en": texts[0].strip(), "brx": texts[1].strip()})
        except Exception:
            pass
        return pairs
