"""
Scrape Glosbe Bodo dictionary for bilingual sentence pairs and words.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bodonlp.scraper.glosbe_scraper import GlosbeScraper


def main():
    print("Testing Glosbe Bodo bilingual scraper...")
    scraper = GlosbeScraper()
    test_words = ["hello", "water", "tree", "father", "friend", "book"]
    
    for w in test_words:
        translations = scraper.fetch_translations(w, from_lang="en", to_lang="brx")
        print(f"Word: '{w}' -> Glosbe Translations: {translations}")

if __name__ == "__main__":
    main()
