# bodonlp · बर' राव (Bodo Language Standard NLP Library)

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/bodonlp/)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-brightgreen.svg)](https://pypi.org/project/bodonlp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language](https://img.shields.io/badge/ISO%20639--3-brx-orange.svg)](https://iso639-3.sil.org/code/brx)
[![FLORES-200 / NLLB](https://img.shields.io/badge/NLLB--200-brx__Deva-red.svg)](https://huggingface.co/facebook/nllb-200-distilled-600M)

A standard-library-style Python package and natural language processing toolkit for the **Bodo Language** (*बड़ो / बर'*, ISO 639-3: `brx`, FLORES/NLLB: `brx_Deva`), an official scheduled language of India spoken predominantly in the Bodoland Territorial Region (BTR) and Assam.

---

## 🌟 Key Highlights

- **36,770+ Offline Dictionary Entries**: Instant, zero-latency multi-way lookups across Bodo (Devanagari), Romanized Bodo, English, and Hindi compiled from official Bodo Sahitya Sabha datasets (*Bihung*).
- **Universal Multi-Engine Translation**: Bidirectional translation between Bodo and English, Hindi, Assamese, and 100+ global languages via local rule-based translation, universal pivot bridging, Hugging Face Meta NLLB-200 / AI4Bharat IndicTrans2, and LLM adapters.
- **Unique Bodo Numeral Classifiers**: Full support for Bodo's classifier system (`सा-` for humans, `मा-` for animals, `गं-` for flat/curved items, `दं-` for tall/cylindrical objects, `थाइ-` for fruits).
- **Agglutinative Morphology & Syntax**: Verb conjugation across 6 tenses/aspects, negation (`-आ` / `-या`), pluralization (`-फोर`), case declension (Accusative `-खौ`, Instrumental `-जों`, Dative `-नो`, Locative `-आव`), and Subject-Object-Verb (SOV) sentence synthesis.
- **Phonetics & Bidirectional Transliteration**: Seamless conversion between Devanagari (*बर' हांखो*) and Romanized/Latin Bodo scripts.
- **Voice AI & Acoustic Cadence**: Syllable stress calculation, high/low pitch tone profiling, and SSML generation for Text-To-Speech (TTS).
- **Cultural Heritage Engine**: Complete encyclopedic repositories of traditional festivals (*Bwisagu, Domashi, Kherai*), musical instruments (*Sifung, Kham, Serja*), attire (*Dokhona, Aronai*), clans/surnames (*Basumatary, Brahma, Narzary*), and sacred Bathou principles.
- **Internet Scrapers & Corpus Mining**: Ready-to-run scraping tools for Bodo Wikipedia / Wikimedia Incubator, Glosbe, and Hugging Face text datasets.

---

## 📦 Installation

### From PyPI:
```bash
pip install bodonlp
```

### From Source (Editable / Development Mode):
```bash
git clone https://github.com/bhupeshjoshi7/bodo.git
cd bodo
pip install -e .
```

---

## 🚀 Quick Start

### 1. Universal Translation
```python
import bodonlp

# Translate English to Bodo (Devanagari + Romanized)
res = bodonlp.translate("Hello, how are you?")
print(res.text)       # मा खबर?
print(res.romanized)  # Ma khobor?
print(res.method)     # rule_based

# Translate Bodo to English
res_en = bodonlp.translate("आं मोजाङैनो दं", target="en")
print(res_en.text)    # I am fine

# Translate between Hindi and Bodo
res_hi = bodonlp.translate("नमस्ते, आप कैसे हैं?", target="brx")
print(res_hi.text)    # खुलुमबाय, मा खबर?
```

### 2. Multi-Way Dictionary Lookup
```python
import bodonlp

# Search by Bodo Devanagari
w1 = bodonlp.lookup("खुलुमबाय")
print(w1.english)   # Hello / Greetings
print(w1.roman)     # Khulumbai
print(w1.pos)       # phrase

# Search by English
w2 = bodonlp.lookup("water")
print(w2.bodo)      # दै
print(w2.roman)     # Dwi

# Search by Romanized Bodo
w3 = bodonlp.lookup("bifang")
print(w3.bodo)      # बिफां (tree)
```

### 3. Numeral System & Classifiers
In Bodo, numerals attach to nouns using specific classifiers:
```python
import bodonlp

# Numbers to words
print(bodonlp.num_to_words(42))                     # 'ब्रैजिनै'
print(bodonlp.num_to_words(42, script="latin"))     # 'brwizinwi'
print(bodonlp.numbers.to_devanagari_numerals(42))   # '४२'

# Classifiers:
# 'सा-' (sa) for humans
print(bodonlp.numbers.apply_classifier("mansi", 1))  # 'सासे मानसि' (one person)
print(bodonlp.numbers.apply_classifier("mansi", 2))  # 'सानै मानसि' (two people)

# 'मा-' (ma) for animals
print(bodonlp.numbers.apply_classifier("swima", 1))  # 'मासे सैमा' (one dog)
print(bodonlp.numbers.apply_classifier("swima", 2))  # 'मानै सैमा' (two dogs)

# 'दं-' (dwng) for trees, rivers, ropes
print(bodonlp.numbers.apply_classifier("tree", 1))   # 'दंसे बिफां' (one tree)
```

### 4. Grammar, Verb Conjugation & Syntax
```python
import bodonlp

# Verb Conjugation (root 'जा' - to eat)
print(bodonlp.conjugate("जा", tense="present"))             # 'जायो' (eats)
print(bodonlp.conjugate("जा", tense="present_continuous"))  # 'जादों' (is eating)
print(bodonlp.conjugate("जा", tense="past"))                # 'जाबाय' (ate / has eaten)
print(bodonlp.conjugate("जा", tense="future"))              # 'जागोन' (will eat)
print(bodonlp.conjugate("जा", tense="present", negative=True)) # 'जाया' (does not eat)

# Pluralization & Case Declension
print(bodonlp.pluralize("मानसि"))                           # 'मानसिफोर' (people)
print(bodonlp.decline_noun("मानसि", bodonlp.constants.Case.ACCUSATIVE))   # 'मानसिखौ' (the person [object])
print(bodonlp.decline_noun("न'", bodonlp.constants.Case.LOCATIVE))       # 'न'आव' (in the house)

# Subject-Object-Verb (SOV) Sentence Construction
sent = bodonlp.build_sentence(subject="आं", object_="ओंखाम", verb="जा", tense="present")
print(sent)  # 'आं ओंखाम जायो।' (I eat rice.)
```

### 5. Phonetics & Transliteration
```python
import bodonlp

# Transliterate Romanized text to Devanagari
dev = bodonlp.transliterate("Khulumbai, ang Boro rao swlwngdwng.", to_script="devanagari")
print(dev)  # 'खुलुमबाय, आं बर' राव सोलोंदों।'

# Transliterate Devanagari to Roman
lat = bodonlp.transliterate("गोजोन फुंबिलि", to_script="latin")
print(lat)  # 'gwjwn fungbili'
```

### 6. Proverbs (फाथास) & Riddles (खानथि)
```python
import bodonlp

# Traditional Proverb
p = bodonlp.random_proverb()
print(p['bodo'])     # गावनि आफाखौ मान हो, गुबुननि आफाखौबो मान हो।
print(p['english'])  # Respect your own father, and respect others' father as well.
print(p['meaning'])  # Treat all elders with equal reverence.

# Traditional Riddle
r = bodonlp.random_riddle()
print(r['question']) # आं जाखाङोब्ला बारायलांगो, आं लोंखाङोब्ला थैयो। आं सोर?
print(r['answer'])   # अर (Or / Fire)
```

### 7. Cultural Heritage
```python
import bodonlp.culture as culture

# Festivals
for f in culture.list_festivals():
    print(f"{f.bodo_name} ({f.name}): {f.significance}")

# Instruments (Sifung, Kham, Serja, etc.)
for inst in culture.list_instruments():
    print(f"{inst.bodo_name} - {inst.instrument_type}")

# Bodo Surnames & Lineages
for clan in culture.list_clans():
    print(f"{clan['devanagari']} ({clan['surname']}): {clan['meaning']}")
```

---

## 💻 Command-Line Interface (CLI)

The library ships with a full CLI tool `bodonlp` (or `bodo-cli`):

```bash
# 1. Translate
bodonlp translate "How are you?"
bodonlp translate "आं मोजाङैनो दं" --target en

# 2. Dictionary Search
bodonlp lookup "खुलुमबाय"
bodonlp lookup "water"
bodonlp search "dance"

# 3. Numbers & Classifiers
bodonlp number 42
bodonlp number 3 --classifier mansi

# 4. Conjugation
bodonlp conjugate "जा" --tense past
bodonlp conjugate "थां" --tense future --negative

# 5. Culture & Heritage
bodonlp culture --festivals
bodonlp culture --instruments
bodonlp culture --clans

# 6. Proverbs & Riddles
bodonlp proverb
bodonlp riddle

# 7. Voice Analysis & SSML
bodonlp voice "Welcome to Bodoland"

# 8. Web Scraping Wikipedia
bodonlp scrape --wiki "बैसागु"

# 9. Library Info
bodonlp info
```

---

## 🌐 Internet Scraping & Corpus Mining Tools

Located in `data_sources/`:
- `data_sources/scrape_wiki_bodo.py`: Scrapes articles from Wikimedia Incubator (`Wp/brx/`) and Bodo Wikipedia, producing clean sentence corpora and vocabulary frequencies.
- `data_sources/scrape_glosbe.py`: Scrapes bilingual dictionary pairs.
- `data_sources/fetch_huggingface_corpus.py`: Streams web-scale Bodo datasets from Hugging Face Hub (`ai4bharat/IndicCorpV2`, FLORES-200).
- `data_sources/ingest_dictionary.py`: Parses and compiles dictionary databases.

---

## 🛠 Publishing to PyPI

To build and publish this library to PyPI:

1. **Install build tools:**
   ```bash
   pip install --upgrade build twine
   ```

2. **Build distribution archives:**
   ```bash
   python -m build
   ```

3. **Check distribution:**
   ```bash
   twine check dist/*
   ```

4. **Upload to PyPI:**
   ```bash
   twine upload dist/*
   ```

---

## 📖 Citation & License

This library is licensed under the [MIT License](LICENSE).

```bibtex
@software{bodonlp2026,
  author = {Bhupesh Joshi},
  title = {bodonlp: Bodo Language Standard NLP Library},
  year = {2026},
  url = {https://github.com/bhupeshjoshi7/bodo}
}
```
