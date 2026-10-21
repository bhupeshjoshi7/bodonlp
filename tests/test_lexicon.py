import unittest
from bodonlp.lexicon import get_lexicon, lookup, search


class TestLexicon(unittest.TestCase):
    def setUp(self):
        self.lex = get_lexicon()

    def test_total_words(self):
        self.assertGreater(self.lex.total_words(), 30000)

    def test_lookup_bodo(self):
        w = lookup("अंखा")
        self.assertIsNotNone(w)
        self.assertEqual(w.bodo, "अंखा")

    def test_lookup_english(self):
        w = lookup("father")
        self.assertIsNotNone(w)

    def test_search(self):
        res = search("culture", limit=5)
        self.assertGreater(len(res), 0)

    def test_proverbs_and_riddles(self):
        proverbs = self.lex.get_proverbs()
        self.assertGreater(len(proverbs), 0)
        
        riddles = self.lex.get_riddles()
        self.assertGreater(len(riddles), 0)


if __name__ == "__main__":
    unittest.main()
