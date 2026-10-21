import unittest
from bodonlp.translator import Translator, translate


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = Translator()

    def test_exact_phrases(self):
        res1 = self.translator.translate("Hello")
        self.assertEqual(res1.text, "खुलुमबाय")
        self.assertEqual(res1.method, "rule_based")

        res2 = self.translator.translate("How are you?")
        self.assertEqual(res2.text, "मा खबर?")

        res3 = self.translator.translate("Thank you")
        self.assertEqual(res3.text, "गोजोन्थों")

    def test_reverse_translation(self):
        res = self.translator.translate("खुलुमबाय", target="en")
        self.assertIn("Hello", res.text)

    def test_sentence_translation(self):
        res = self.translator.translate("I eat rice")
        self.assertTrue(len(res.text) > 0)
        self.assertIn("आं", res.text)

    def test_convenience_function(self):
        res = translate("good morning")
        self.assertEqual(res.text, "गोजोन फुंबिलि")


if __name__ == "__main__":
    unittest.main()
