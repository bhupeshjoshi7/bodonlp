# Bodo NLP Data Sources & Corpus Mining Pipeline

This directory contains ingestion, web scraping, and dataset curation scripts used to compile and expand the digital corpus and dictionary of the **Bodo Language (`brx`)**.

---

## 1. Primary Data Sources

| Source | Domain / Scope | Status in Library | Entries / Size |
| :--- | :--- | :--- | :--- |
| **Bihung (Bodo Sahitya Sabha)** | General vocabulary & subject glossaries (Archeology, Geology, CS, etc.) | Fully Ingested | **36,777 words** |
| **Bodo Wikipedia (brx / Incubator)** | Encyclopedia articles, prose, sentences | Scraped via MediaWiki API | 167+ verified sentences |
| **Glosbe Bodo-English** | Crowd-sourced bilingual phrases & idioms | Scraper provided | Real-time lookup |
| **Hugging Face (`ai4bharat/IndicCorpV2`, FLORES-200)** | Web-scale Bodo parallel & monolingual corpus | Downloader pipeline | Streamable |

---

## 2. Ingestion & Mining Scripts

### `ingest_dictionary.py`
Parses raw dictionary dumps from Bihung, normalizes Devanagari Unicode, generates phonetic Romanizations, extracts parts of speech, and outputs the primary production database:
```bash
python data_sources/ingest_dictionary.py
```
Outputs: `bodonlp/lexicon/data/words.json` (~6.7 MB).

### `build_cultural_datasets.py`
Compiles curated conversational phrases, traditional Bodo proverbs (*फाथास*), and authentic riddles (*खानथि*):
```bash
python data_sources/build_cultural_datasets.py
```

### `scrape_wiki_bodo.py`
Queries the MediaWiki API on `brx.wikipedia.org` and Wikimedia Incubator (`Wp/brx/`), extracting plain text, stripping markup, splitting sentences, and computing word frequencies:
```bash
python data_sources/scrape_wiki_bodo.py
```

### `scrape_glosbe.py`
Scrapes Glosbe for bilingual translation alternatives and contextual sentence examples:
```bash
python data_sources/scrape_glosbe.py
```

### `fetch_huggingface_corpus.py`
Streams large-scale Bodo datasets from Hugging Face Hub using the `datasets` library:
```bash
python data_sources/fetch_huggingface_corpus.py
```
