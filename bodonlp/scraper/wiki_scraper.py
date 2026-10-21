"""
Bodo Wikipedia & Wikimedia Scraper.
Extracts articles, clean text corpus, and vocabulary from Bodo Wikipedia (brx.wikipedia.org).
"""

import json
import re
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional
from pathlib import Path


class WikiScraper:
    def __init__(self, user_agent: str = "BodoNLPLibrary/1.0 (https://github.com/bhupeshjoshi7/bodo)"):
        self.api_url = "https://brx.wikipedia.org/w/api.php"
        self.incubator_api_url = "https://incubator.wikimedia.org/w/api.php"
        self.user_agent = user_agent

    def _query(self, params: Dict[str, str], use_incubator: bool = False) -> Dict[str, Any]:
        """Send request to MediaWiki API."""
        base_url = self.incubator_api_url if use_incubator else self.api_url
        params["format"] = "json"
        query_string = urllib.parse.urlencode(params)
        full_url = f"{base_url}?{query_string}"
        
        req = urllib.request.Request(full_url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}

    def search_articles(self, query: str, limit: int = 10) -> List[Dict[str, str]]:
        """Search articles on Bodo Wikipedia or Wikimedia Incubator."""
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": str(limit),
        }
        res = self._query(params, use_incubator=False)
        search_results = res.get("query", {}).get("search", [])
        
        # If no results on brx.wikipedia.org, query Wikimedia Incubator with prefix Wp/brx
        if not search_results:
            inc_params = {
                "action": "query",
                "list": "search",
                "srsearch": f"Wp/brx/{query}",
                "srlimit": str(limit),
            }
            inc_res = self._query(inc_params, use_incubator=True)
            search_results = inc_res.get("query", {}).get("search", [])

        return [
            {
                "title": r.get("title", ""),
                "snippet": re.sub(r'<[^>]+>', '', r.get("snippet", "")),
                "pageid": r.get("pageid", "")
            }
            for r in search_results
        ]

    def get_article_text(self, title: str) -> Optional[str]:
        """Fetch the plain text content of a Bodo Wikipedia or Incubator article."""
        use_inc = title.startswith("Wp/brx") or "incubator" in title.lower()
        params = {
            "action": "query",
            "prop": "extracts",
            "explaintext": "1",
            "titles": title,
        }
        res = self._query(params, use_incubator=use_inc)
        pages = res.get("query", {}).get("pages", {})
        for _, page in pages.items():
            if "extract" in page:
                return page["extract"]
        return None

    def scrape_corpus(self, topic: str = "बर'", max_articles: int = 5, save_to_dir: Optional[Path] = None) -> List[Dict[str, str]]:
        """
        Scrape a batch of articles related to a topic and optionally save to disk as corpus.
        """
        articles = self.search_articles(topic, limit=max_articles)
        corpus = []
        
        for art in articles:
            title = art["title"]
            text = self.get_article_text(title)
            if text:
                entry = {"title": title, "text": text}
                corpus.append(entry)
                
                if save_to_dir:
                    save_to_dir = Path(save_to_dir)
                    save_to_dir.mkdir(parents=True, exist_ok=True)
                    safe_title = re.sub(r'[\/:*?"<>|]', '_', title)
                    file_path = save_to_dir / f"{safe_title}.txt"
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(text)

        return corpus
