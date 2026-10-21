import unittest
from bodonlp.constants import (
    ISO_639_3,
    ISO_639_NAME,
    NATIVE_NAME,
    NLLB_CODE,
    Case,
    CASE_MARKERS,
    NUMERAL_CLASSIFIERS,
)


class TestConstants(unittest.TestCase):
    def test_iso_codes(self):
        self.assertEqual(ISO_639_3, "brx")
        self.assertEqual(ISO_639_NAME, "Bodo")
        self.assertEqual(NLLB_CODE, "brx_Deva")
        self.assertIn("बड़ो", NATIVE_NAME)

    def test_case_markers(self):
        self.assertIn(Case.ACCUSATIVE, CASE_MARKERS)
        self.assertEqual(CASE_MARKERS[Case.ACCUSATIVE]["marker"], "खौ")
        self.assertEqual(CASE_MARKERS[Case.INSTRUMENTAL]["marker"], "जों")
        self.assertEqual(CASE_MARKERS[Case.DATIVE]["marker"], "नो")
        self.assertEqual(CASE_MARKERS[Case.LOCATIVE]["marker"], "आव")

    def test_numeral_classifiers(self):
        self.assertIn("sa", NUMERAL_CLASSIFIERS)
        self.assertIn("ma", NUMERAL_CLASSIFIERS)
        self.assertIn("gwng", NUMERAL_CLASSIFIERS)
        self.assertEqual(NUMERAL_CLASSIFIERS["sa"]["marker"], "सा")
        self.assertEqual(NUMERAL_CLASSIFIERS["ma"]["marker"], "मा")


if __name__ == "__main__":
    unittest.main()
