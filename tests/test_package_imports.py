import unittest


class TestPackageImports(unittest.TestCase):
    def test_import_bodo_language_library(self):
        import bodo_language_library as bodo
        res = bodo.translate("Hello")
        self.assertEqual(res.text, "खुलुमबाय")
        w = bodo.lookup("water")
        self.assertEqual(w.bodo, "दै")

    def test_import_bodonlp(self):
        import bodonlp
        res = bodonlp.translate("Good morning")
        self.assertEqual(res.text, "गोजोन फुंबिलि")

    def test_import_bodo_lang(self):
        import bodo_lang
        res = bodo_lang.translate("Thank you")
        self.assertEqual(res.text, "गोजोन्थों")


if __name__ == "__main__":
    unittest.main()
