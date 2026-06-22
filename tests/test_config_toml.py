import unittest
import tomllib
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.toml"


class TestConfigToml(unittest.TestCase):

    def setUp(self):
        with open(CONFIG_PATH, "rb") as f:
            self.config = tomllib.load(f)

    def test_teams_key_exists(self):
        self.assertIn("teams", self.config)
        self.assertIn("names", self.config["teams"])

    def test_teams_count_is_18(self):
        self.assertEqual(len(self.config["teams"]["names"]), 18)

    def test_no_duplicate_teams(self):
        names = self.config["teams"]["names"]
        self.assertEqual(len(names), len(set(names)))

    def test_all_entries_are_nonempty_strings(self):
        for name in self.config["teams"]["names"]:
            self.assertIsInstance(name, str)
            self.assertTrue(len(name.strip()) > 0)
