import unittest
from bodonlp.grammar import (
    conjugate,
    pluralize,
    decline_noun,
    get_pronoun,
    build_sentence,
    echo_word,
)
from bodonlp.constants import Case


class TestGrammar(unittest.TestCase):
    def test_verb_conjugation(self):
        # Present Indefinite
        self.assertEqual(conjugate("जा", "present"), "जायो")
        # Continuous
        self.assertEqual(conjugate("जा", "present_continuous"), "जादों")
        # Past
        self.assertEqual(conjugate("जा", "past"), "जाबाय")
        # Future
        self.assertEqual(conjugate("जा", "future"), "जागोन")
        # Negation
        self.assertEqual(conjugate("जा", "present", negative=True), "जाया")
        self.assertEqual(conjugate("थां", "present", negative=True), "थाङा")

    def test_noun_pluralization(self):
        self.assertEqual(pluralize("मानसि"), "मानसिफोर")
        self.assertEqual(pluralize("सैमा"), "सैमाफोर")

    def test_noun_declension(self):
        self.assertEqual(decline_noun("मानसि", Case.ACCUSATIVE), "मानसिखौ")
        self.assertEqual(decline_noun("मानसि", Case.INSTRUMENTAL), "मानसिजों")
        self.assertEqual(decline_noun("मानसि", Case.DATIVE), "मानसिनो")
        self.assertEqual(decline_noun("न'", Case.LOCATIVE), "न'आव")

    def test_pronouns(self):
        self.assertEqual(get_pronoun(1, plural=False, case="nom"), "आं")
        self.assertEqual(get_pronoun(1, plural=False, case="acc"), "आंखौ")
        self.assertEqual(get_pronoun(2, plural=False, case="nom"), "नों")
        self.assertEqual(get_pronoun(3, plural=False, case="nom"), "बियो")
        self.assertEqual(get_pronoun(1, plural=True, case="nom"), "जों")

    def test_sentence_builder(self):
        sent = build_sentence("आं", "ओंखाम", "जा", tense="present")
        self.assertEqual(sent, "आं ओंखाम जायो।")
        
        q_sent = build_sentence("नों", "ओंखाम", "जा", tense="past", interrogative=True)
        self.assertEqual(q_sent, "नों ओंखाम जाबायना?")

    def test_echo_word(self):
        self.assertEqual(echo_word("हाबा"), "हाबा-हुखा")


if __name__ == "__main__":
    unittest.main()
