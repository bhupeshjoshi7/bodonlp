import unittest
import subprocess
import sys


class TestCLI(unittest.TestCase):
    def test_cli_info(self):
        res = subprocess.run(
            [sys.executable, "-m", "bodonlp.cli", "info"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("Bodo Language Library", res.stdout)
        self.assertIn("brx", res.stdout)

    def test_cli_translate(self):
        res = subprocess.run(
            [sys.executable, "-m", "bodonlp.cli", "translate", "Hello"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("खुलुमबाय", res.stdout)

    def test_cli_lookup(self):
        res = subprocess.run(
            [sys.executable, "-m", "bodonlp.cli", "lookup", "father"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("Bodo", res.stdout)

    def test_cli_number(self):
        res = subprocess.run(
            [sys.executable, "-m", "bodonlp.cli", "number", "42"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("४२", res.stdout)
        self.assertIn("ब्रैजिनै", res.stdout)


if __name__ == "__main__":
    unittest.main()
