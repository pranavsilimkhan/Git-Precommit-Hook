# test_cli.py
import unittest
from cli import regexCheck

class TestRegexCheck(unittest.TestCase):

    def test_with_secret(self):
        self.assertTrue(regexCheck("my secret = 'SuperSecret123'", "test_file"))

    def test_with_password(self):
        self.assertTrue(regexCheck("password: 'Pa$$word'", "test_file"))

    def test_with_api_key(self):
        self.assertTrue(regexCheck("API_KEY='ABCDEF1234567890'", "test_file"))

    def test_with_long_string(self):
        self.assertTrue(regexCheck("Random string XYZ1234567890", "test_file"))

    def test_without_secret(self):
        self.assertFalse(regexCheck("Just some regular text here.", "test_file"))

    def test_with_short_secret(self):
        self.assertFalse(regexCheck("secret = 'short'", "test_file"))

if __name__ == '__main__':
    unittest.main()
