"""
Scrape Bodo Wikipedia articles to expand local corpus and dictionary entries.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bodonlp.scraper.wiki_scraper import WikiScraper
from bodonlp.scraper.corpus_collector import CorpusCollector

def main():
    print("Initializing Bodo Wikipedia Scraper...")
    scraper = WikiScraper()
    collector = CorpusCollector(output_dir=ROOT / "data_sources" / "raw_texts")
    
    topics = ["बर'", "बाथौ", "बैसागु", "आसाम", "सिफुं", "बसुमतारि"]
    all_sentences = []
    
    for t in topics:
        print(f"\nSearching articles for topic: '{t}'...")
        articles = scraper.scrape_corpus(topic=t, max_articles=3, save_to_dir=ROOT / "data_sources" / "raw_texts")
        for art in articles:
            sents = collector.extract_sentences(art["text"])
            all_sentences.extend(sents)
            print(f"  - '{art['title']}': extracted {len(sents)} sentences.")
            
    if all_sentences:
        collector.save_corpus_file("bodo_wiki_sentences.txt", all_sentences)
        vocab = collector.build_vocabulary(all_sentences)
        print(f"Extracted vocabulary size: {len(vocab)} unique words.")
        top_words = list(vocab.items())[:15]
        print(f"Top 15 most frequent words in scraped corpus: {top_words}")
    else:
        print("No articles fetched or network unavailable.")

if __name__ == "__main__":
    main()
