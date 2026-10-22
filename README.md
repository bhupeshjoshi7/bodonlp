# bodo_language_library · बर' राव (Bodo Language Standard Library)

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/bodo_language_library/)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-brightgreen.svg)](https://pypi.org/project/bodo_language_library/)
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
pip install bodo_language_library
```

*(Note: You can also use `pip install bodonlp`).*

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
import bodo_language_library as bodo

# Translate English to Bodo (Devanagari + Romanized)
res = bodo.translate("Hello, how are you?")
print(res.text)       # मा खबर?
print(res.romanized)  # Ma khobor?
print(res.method)     # rule_based

# Translate Bodo to English
res_en = bodo.translate("आं मोजाङैनो दं", target="en")
print(res_en.text)    # I am fine

# Translate between Hindi and Bodo
res_hi = bodo.translate("नमस्ते, आप कैसे हैं?", target="brx")
print(res_hi.text)    # खुलुमबाय, मा खबर?
```

### 2. Multi-Way Dictionary Lookup
```python
import bodo_language_library as bodo

# Search by Bodo Devanagari
w1 = bodo.lookup("खुलुमबाय")
print(w1.english)   # Hello / Greetings
print(w1.roman)     # Khulumbai
print(w1.pos)       # phrase

# Search by English
w2 = bodo.lookup("water")
print(w2.bodo)      # दै
print(w2.roman)     # Dwi

# Search by Romanized Bodo
w3 = bodo.lookup("bifang")
print(w3.bodo)      # बिफां (tree)
```

### 3. Numeral System & Classifiers
In Bodo, numerals attach to nouns using specific classifiers:
```python
import bodo_language_library as bodo

# Numbers to words
print(bodo.num_to_words(42))                     # 'ब्रैजिनै'
print(bodo.num_to_words(42, script="latin"))     # 'brwizinwi'
print(bodo.numbers.to_devanagari_numerals(42))   # '४२'

# Classifiers:
# 'सा-' (sa) for humans
print(bodo.numbers.apply_classifier("mansi", 1))  # 'सासे मानसि' (one person)
print(bodo.numbers.apply_classifier("mansi", 2))  # 'सानै मानसि' (two people)

# 'मा-' (ma) for animals
print(bodo.numbers.apply_classifier("swima", 1))  # 'मासे सैमा' (one dog)
print(bodo.numbers.apply_classifier("swima", 2))  # 'मानै सैमा' (two dogs)

# 'दं-' (dwng) for trees, rivers, ropes
print(bodo.numbers.apply_classifier("tree", 1))   # 'दंसे बिफां' (one tree)
```

### 4. Grammar, Verb Conjugation & Syntax
```python
import bodo_language_library as bodo

# Verb Conjugation (root 'जा' - to eat)
print(bodo.conjugate("जा", tense="present"))             # 'जायो' (eats)
print(bodo.conjugate("जा", tense="present_continuous"))  # 'जादों' (is eating)
print(bodo.conjugate("जा", tense="past"))                # 'जाबाय' (ate / has eaten)
print(bodo.conjugate("जा", tense="future"))              # 'जागोन' (will eat)
print(bodo.conjugate("जा", tense="present", negative=True)) # 'जाया' (does not eat)

# Pluralization & Case Declension
print(bodo.pluralize("मानसि"))                           # 'मानसिफोर' (people)
print(bodo.decline_noun("मानसि", bodo.constants.Case.ACCUSATIVE))   # 'मानसिखौ' (the person [object])
print(bodo.decline_noun("न'", bodo.constants.Case.LOCATIVE))       # 'न'आव' (in the house)

# Subject-Object-Verb (SOV) Sentence Construction
sent = bodo.build_sentence(subject="आं", object_="ओंखाम", verb="जा", tense="present")
print(sent)  # 'आं ओंखाम जायो।' (I eat rice.)
```

### 5. Phonetics & Transliteration
```python
import bodo_language_library as bodo

# Transliterate Romanized text to Devanagari
dev = bodo.transliterate("Khulumbai, ang Boro rao swlwngdwng.", to_script="devanagari")
print(dev)  # 'खुलुमबाय, आं बर' राव सोलोंदों।'

# Transliterate Devanagari to Roman
lat = bodo.transliterate("गोजोन फुंबिलि", to_script="latin")
print(lat)  # 'gwjwn fungbili'
```

### 6. Proverbs (फाथास) & Riddles (खानथि)
```python
import bodo_language_library as bodo

# Traditional Proverb
p = bodo.random_proverb()
print(p['bodo'])     # गावनि आफाखौ मान हो, गुबुननि आफाखौबो मान हो।
print(p['english'])  # Respect your own father, and respect others' father as well.
print(p['meaning'])  # Treat all elders with equal reverence.

# Traditional Riddle
r = bodo.random_riddle()
print(r['question']) # आं जाखाङोब्ला बारायलांगो, आं लोंखाङोब्ला थैयो। आं सोर?
print(r['answer'])   # अर (Or / Fire)
```

### 7. Cultural Heritage
```python
import bodo_language_library.culture as culture

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

The library provides the `bodo` (or `bodonlp`) command-line tool:

```bash
# 1. Translate
bodo translate "How are you?"
bodo translate "आं मोजाङैनो दं" --target en

# 2. Dictionary Search
bodo lookup "खुलुमबाय"
bodo lookup "water"
bodo search "dance"

# 3. Numbers & Classifiers
bodo number 42
bodo number 3 --classifier mansi

# 4. Conjugation
bodo conjugate "जा" --tense past
bodo conjugate "थां" --tense future --negative

# 5. Culture & Heritage
bodo culture --festivals
bodo culture --instruments
bodo culture --clans

# 6. Proverbs & Riddles
bodo proverb
bodo riddle

# 7. Voice Analysis & SSML
bodo voice "Welcome to Bodoland"

# 8. Web Scraping Wikipedia
bodo scrape --wiki "बैसागु"

# 9. Library Info
bodo info
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
   python setup.py sdist bdist_wheel
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
@software{bodo_language_library2026,
  author = {Bhupesh Joshi},
  title = {bodo_language_library: Bodo Language Standard Library},
  year = {2026},
  url = {https://github.com/bhupeshjoshi7/bodo}
}
```
