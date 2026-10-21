import unittest
from bodonlp.numbers import (
    num_to_words,
    words_to_num,
    to_devanagari_numerals,
    from_devanagari_numerals,
    ordinal,
    fraction,
    apply_classifier,
)


class TestNumbers(unittest.TestCase):
    def test_num_to_words(self):
        self.assertEqual(num_to_words(0), "लाथिख'")
        self.assertEqual(num_to_words(1), "से")
        self.assertEqual(num_to_words(2), "नै")
        self.assertEqual(num_to_words(5), "बा")
        self.assertEqual(num_to_words(10), "जि")
        self.assertEqual(num_to_words(14), "जिब्रै")
        self.assertEqual(num_to_words(20), "नैजि")
        self.assertEqual(num_to_words(42), "ब्रैजिनै")
        self.assertEqual(num_to_words(100), "जौसे")
        self.assertEqual(num_to_words(1000), "रोजासे")

    def test_romanized_numbers(self):
        self.assertEqual(num_to_words(1, script="latin"), "se")
        self.assertEqual(num_to_words(2, script="latin"), "nwi")
        self.assertEqual(num_to_words(10, script="latin"), "zi")

    def test_numerals(self):
        self.assertEqual(to_devanagari_numerals(42), "४२")
        self.assertEqual(from_devanagari_numerals("४२"), 42)

    def test_ordinals(self):
        self.assertEqual(ordinal(1), "सेथि")
        self.assertEqual(ordinal(2), "नैथि")

    def test_classifiers(self):
        # Human classifier सा-
        c_person = apply_classifier("मानसि", 1)
        self.assertEqual(c_person, "सासे मानसि")
        
        # Animal classifier मा-
        c_animal = apply_classifier("सैमा", 2)
        self.assertEqual(c_animal, "मानै सैमा")
        
        # Long object classifier दं-
        c_tree = apply_classifier("बिफां", 1)
        self.assertEqual(c_tree, "दंसे बिफां")


if __name__ == "__main__":
    unittest.main()
