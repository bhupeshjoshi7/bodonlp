"""
Bodo Web Scraping and Corpus Mining Package.
"""

from bodonlp.scraper.wiki_scraper import WikiScraper
from bodonlp.scraper.glosbe_scraper import GlosbeScraper
from bodonlp.scraper.corpus_collector import CorpusCollector

__all__ = [
    "WikiScraper",
    "GlosbeScraper",
    "CorpusCollector",
]
