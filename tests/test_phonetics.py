import unittest
from bodonlp.phonetics import (
    normalize_devanagari,
    detect_script,
    devanagari_to_latin,
    latin_to_devanagari,
    syllables,
)
from bodonlp.constants import Script


class TestPhonetics(unittest.TestCase):
    def test_script_detection(self):
        self.assertEqual(detect_script("बर' राव"), Script.DEVANAGARI)
        self.assertEqual(detect_script("Boro rao"), Script.LATIN)

    def test_normalization(self):
        self.assertEqual(normalize_devanagari("बर’"), "बर'")
        self.assertEqual(normalize_devanagari("गथ‘"), "गथ'")

    def test_devanagari_to_latin(self):
        res = devanagari_to_latin("मोजां")
        self.assertTrue(len(res) > 0)
        self.assertIn("m", res.lower())

    def test_latin_to_devanagari(self):
        self.assertEqual(latin_to_devanagari("khulumbai"), "खुलुमबाय")
        self.assertEqual(latin_to_devanagari("ang"), "आं")
        self.assertEqual(latin_to_devanagari("nwng"), "नों")

    def test_syllables(self):
        syls = syllables("खुलुमबाय")
        self.assertTrue(len(syls) >= 2)


if __name__ == "__main__":
    unittest.main()
