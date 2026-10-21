"""
Command-Line Interface (CLI) for the Bodo Language Library (bodonlp).
Usage:
    bodonlp translate "Hello, how are you?"
    bodonlp lookup "खुलुमबाय"
    bodonlp number 42
    bodonlp conjugate "जा" --tense past
    bodonlp proverb
    bodonlp riddle
    bodonlp voice "Welcome to our village"
    bodonlp culture --festivals
    bodonlp transliterate "Khulumbai" --to devanagari
"""

import sys
import argparse
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import bodonlp
from bodonlp.constants import (
    ISO_639_3,
    ISO_639_NAME,
    NATIVE_NAME,
    NATIVE_NAME_ALT,
    NLLB_CODE,
    Case,
)


def main():
    parser = argparse.ArgumentParser(
        prog="bodonlp",
        description="Bodo Language Standard NLP Library CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # translate
    trans_parser = subparsers.add_parser("translate", help="Translate text to and from Bodo")
    trans_parser.add_argument("text", type=str, help="Text to translate")
    trans_parser.add_argument("--source", "-s", default="auto", help="Source language (default: auto)")
    trans_parser.add_argument("--target", "-t", default="brx", help="Target language (default: brx)")
    trans_parser.add_argument("--method", "-m", default="auto", choices=["auto", "rule_based", "pivot", "hf", "llm"])
    trans_parser.add_argument("--api-key", "-k", default=None, help="Optional Gemini/OpenAI API key")

    # lookup
    lookup_parser = subparsers.add_parser("lookup", help="Dictionary lookup across Bodo, English, and Hindi")
    lookup_parser.add_argument("word", type=str, help="Word to look up")

    # search
    search_parser = subparsers.add_parser("search", help="Fuzzy and substring search in dictionary")
    search_parser.add_argument("query", type=str, help="Query string")
    search_parser.add_argument("--limit", "-l", type=int, default=5, help="Max results (default: 5)")

    # number
    num_parser = subparsers.add_parser("number", help="Convert numbers to Bodo words or numerals")
    num_parser.add_argument("num", type=int, help="Integer to convert")
    num_parser.add_argument("--script", default="devanagari", choices=["devanagari", "latin"])
    num_parser.add_argument("--classifier", "-c", default=None, help="Attach classifier for noun (e.g., 'mansi', 'dog')")

    # conjugate
    conj_parser = subparsers.add_parser("conjugate", help="Conjugate Bodo verbs")
    conj_parser.add_argument("verb", type=str, help="Verb root (e.g., जा, थां, eat, go)")
    conj_parser.add_argument("--tense", "-t", default="present", choices=["present", "present_continuous", "past", "past_continuous", "future", "imperative"])
    conj_parser.add_argument("--negative", "-n", action="store_true", help="Negate verb")
    conj_parser.add_argument("--script", default="devanagari", choices=["devanagari", "latin"])

    # proverb
    subparsers.add_parser("proverb", help="Display a traditional Bodo proverb (फाथास / Bathra Sao)")

    # riddle
    subparsers.add_parser("riddle", help="Display a traditional Bodo riddle (खानथि / Sol)")

    # voice
    voice_parser = subparsers.add_parser("voice", help="Speech translation with syllables, stress, and SSML")
    voice_parser.add_argument("text", type=str, help="Text to translate for voice synthesis")
    voice_parser.add_argument("--source", "-s", default="auto", help="Source language (default: auto)")

    # transliterate
    translit_parser = subparsers.add_parser("transliterate", help="Transliterate between Devanagari and Latin")
    translit_parser.add_argument("text", type=str, help="Text to transliterate")
    translit_parser.add_argument("--to", default="devanagari", choices=["devanagari", "latin"])

    # culture
    culture_parser = subparsers.add_parser("culture", help="Explore Bodo festivals, attire, instruments, and clans")
    culture_parser.add_argument("--festivals", action="store_true", help="List traditional festivals")
    culture_parser.add_argument("--instruments", action="store_true", help="List musical instruments")
    culture_parser.add_argument("--attire", action="store_true", help="List traditional clothing")
    culture_parser.add_argument("--clans", action="store_true", help="List Bodo clans and surnames")
    culture_parser.add_argument("--bathou", action="store_true", help="Explain Bathou principles")

    # scrape
    scrape_parser = subparsers.add_parser("scrape", help="Scrape articles and text from Bodo Wikipedia")
    scrape_parser.add_argument("--wiki", type=str, default="बैसागु", help="Wikipedia topic to scrape")
    scrape_parser.add_argument("--max", type=int, default=2, help="Max articles")

    # info
    subparsers.add_parser("info", help="Library details, dictionary statistics, and ISO codes")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "translate":
        res = bodonlp.translate(args.text, source=args.source, target=args.target, method=args.method, api_key=args.api_key)
        print(f"\n[Source ({res.source_lang})]: {res.source}")
        print(f"[Translation ({res.target_lang})]: {res.text}")
        if res.romanized:
            print(f"[Romanized]:          {res.romanized}")
        print(f"[Method]:             {res.method} (confidence: {res.confidence:.2f})\n")

    elif args.command == "lookup":
        w = bodonlp.lookup(args.word)
        if w:
            print(f"\nBodo (बर'):    {w.bodo} ({w.roman})")
            print(f"English:       {w.english}")
            if w.hindi:
                print(f"Hindi:         {w.hindi}")
            print(f"POS:           {w.pos}")
            print(f"Domain:        {w.category}\n")
        else:
            print(f"\nNo exact entry found for '{args.word}'. Try `bodonlp search {args.word}`.\n")

    elif args.command == "search":
        results = bodonlp.search(args.query, limit=args.limit)
        print(f"\nFound {len(results)} matches for '{args.query}':")
        for i, w in enumerate(results, 1):
            print(f" {i}. {w.bodo} ({w.roman}) - {w.english} [{w.category}]")
        print()

    elif args.command == "number":
        if args.classifier:
            res = bodonlp.numbers.apply_classifier(args.classifier, args.num, script=args.script)
            print(f"\n{args.num} classified with '{args.classifier}': {res}\n")
        else:
            w = bodonlp.num_to_words(args.num, script=args.script)
            dev_num = bodonlp.numbers.to_devanagari_numerals(args.num)
            print(f"\nInteger:     {args.num}")
            print(f"Bodo Numerals: {dev_num}")
            print(f"In Words:      {w}\n")

    elif args.command == "conjugate":
        res = bodonlp.conjugate(args.verb, tense=args.tense, negative=args.negative, script=args.script)
        pol = "Negative" if args.negative else "Positive"
        print(f"\nVerb: '{args.verb}' | Tense: {args.tense} | Polarity: {pol}")
        print(f"Conjugated: {res}\n")

    elif args.command == "transliterate":
        res = bodonlp.transliterate(args.text, to_script=args.to)
        print(f"\nInput:      {args.text}")
        print(f"Output ({args.to}): {res}\n")

    elif args.command == "proverb":
        p = bodonlp.random_proverb()
        if p:
            print(f"\n[Bodo Proverb (फाथास)]")
            print(f"बर':    {p['bodo']}")
            print(f"Roman:  {p['roman']}")
            print(f"English: {p['english']}")
            print(f"Meaning: {p['meaning']}\n")

    elif args.command == "riddle":
        r = bodonlp.random_riddle()
        if r:
            print(f"\n[Bodo Riddle (खानथि)]")
            print(f"क्वेश्चन: {r['question']}")
            print(f"Roman:   {r['roman']}")
            print(f"English: {r['english']}")
            print(f"Hint:    {r.get('hint', '')}")
            print(f"Answer:  {r['answer']}\n")

    elif args.command == "voice":
        res = bodonlp.voice.translate_for_voice(args.text, source_lang=args.source)
        print(f"\n[Spoken Input]:    {res.source_text}")
        print(f"[Bodo Voice Text]: {res.translated_text}")
        print(f"[Phonetic Cadence]:{res.romanized}")
        print(f"[Syllables]:       {' · '.join(res.syllables)}")
        print(f"[Tone Profile]:    {res.tone_profile}")
        print(f"[SSML]:            {res.ssml}\n")

    elif args.command == "culture":
        if args.festivals or (not args.instruments and not args.attire and not args.clans and not args.bathou):
            print("\n=== Traditional Bodo Festivals ===")
            for f in bodonlp.culture.list_festivals():
                print(f"• {f.bodo_name} ({f.name}) - {f.timing}")
                print(f"  {f.significance}")
            print()
        if args.instruments:
            print("\n=== Traditional Bodo Musical Instruments ===")
            for inst in bodonlp.culture.list_instruments():
                print(f"• {inst.bodo_name} ({inst.name}) - {inst.instrument_type}")
                print(f"  {inst.cultural_use}")
            print()
        if args.attire:
            print("\n=== Traditional Bodo Attire ===")
            for a in bodonlp.culture.list_attire():
                print(f"• {a.bodo_name} ({a.name}) [{a.gender}]")
                print(f"  {a.description}")
            print()
        if args.clans:
            print("\n=== Prominent Bodo Clans & Surnames ===")
            for c in bodonlp.culture.list_clans():
                print(f"• {c['devanagari']} ({c['surname']}): {c['meaning']}")
            print()
        if args.bathou:
            b = bodonlp.culture.get_bathou_principles()
            print("\n=== Sacred Bathou Principles ===")
            print(f"Deity: {b['deity']}")
            print(f"Sacred Tree: {b['sacred_plant']}")
            print("Five Moral Bamboo Rings:")
            for r in b['five_bamboo_rings']:
                print(f"  {r['ring']}. {r['principle']}")
            print()

    elif args.command == "scrape":
        print(f"\nScraping Bodo Wikipedia articles for: '{args.wiki}'...")
        scraper = bodonlp.scraper.WikiScraper()
        articles = scraper.scrape_corpus(topic=args.wiki, max_articles=args.max)
        if articles:
            for a in articles:
                print(f"\nTitle: {a['title']}")
                print(f"Excerpt: {a['text'][:200]}...\n")
        else:
            print("No articles found or network unavailable.\n")

    elif args.command == "info":
        lex = bodonlp.get_lexicon()
        print("\n=============================================")
        print(f"  Bodo Language Library (bodonlp)")
        print("=============================================")
        print(f"Language:            {ISO_639_NAME} ({NATIVE_NAME} / {NATIVE_NAME_ALT})")
        print(f"ISO 639-3 Code:      {ISO_639_3}")
        print(f"FLORES / NLLB Code:  {NLLB_CODE}")
        print(f"Dictionary Entries:  {lex.total_words():,} words")
        print(f"Proverbs & Riddles:  {len(lex.get_proverbs())} proverbs, {len(lex.get_riddles())} riddles")
        print(f"Phrases Bundled:     {len(lex.get_phrases())} conversational pairs")
        print("Status:              Ready for PyPI distribution")
        print("=============================================\n")


if __name__ == "__main__":
    main()
