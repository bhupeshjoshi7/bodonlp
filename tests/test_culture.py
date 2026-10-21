import unittest
from bodonlp.culture import (
    list_festivals,
    get_festival,
    list_instruments,
    list_attire,
    list_clans,
    get_bathou_principles,
)


class TestCulture(unittest.TestCase):
    def test_festivals(self):
        festivals = list_festivals()
        self.assertGreaterEqual(len(festivals), 5)
        bwisagu = get_festival("Bwisagu")
        self.assertIsNotNone(bwisagu)
        self.assertEqual(bwisagu.bodo_name, "बैसागु")

    def test_instruments(self):
        insts = list_instruments()
        self.assertTrue(any(i.bodo_name == "सिफुं" for i in insts))
        self.assertTrue(any(i.bodo_name == "खाम" for i in insts))

    def test_attire(self):
        attires = list_attire()
        self.assertTrue(any(a.bodo_name == "दखना" for a in attires))
        self.assertTrue(any(a.bodo_name == "आरोनाइ" for a in attires))

    def test_clans(self):
        clans = list_clans()
        self.assertTrue(any(c["surname"] == "Basumatary" for c in clans))
        self.assertTrue(any(c["surname"] == "Brahma" for c in clans))

    def test_bathou(self):
        bathou = get_bathou_principles()
        self.assertIn("Bathoubwrai", bathou["deity"])
        self.assertEqual(len(bathou["five_bamboo_rings"]), 5)


if __name__ == "__main__":
    unittest.main()
