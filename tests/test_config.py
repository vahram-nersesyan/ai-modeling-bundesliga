import unittest

from src.config import NUM_TEAMS, NUM_MATCHDAYS, SEASON_SPLIT, TEAMS


class TestDerivedConstants(unittest.TestCase):

    def test_num_teams(self):
        self.assertEqual(NUM_TEAMS, 18)

    def test_num_matchdays(self):
        self.assertEqual(NUM_MATCHDAYS, (NUM_TEAMS - 1) * 2)
        self.assertEqual(NUM_MATCHDAYS, 34)

    def test_season_split(self):
        self.assertEqual(SEASON_SPLIT, NUM_MATCHDAYS // 2)
        self.assertEqual(SEASON_SPLIT, 17)

    def test_teams_is_list_from_config(self):
        self.assertIsInstance(TEAMS, list)
        self.assertEqual(len(TEAMS), 18)


class TestDerivationFormula(unittest.TestCase):

    def test_four_teams(self):
        n = 4
        self.assertEqual((n - 1) * 2, 6)
        self.assertEqual(((n - 1) * 2) // 2, 3)

    def test_six_teams(self):
        n = 6
        self.assertEqual((n - 1) * 2, 10)
        self.assertEqual(((n - 1) * 2) // 2, 5)

    def test_twenty_teams(self):
        n = 20
        self.assertEqual((n - 1) * 2, 38)
        self.assertEqual(((n - 1) * 2) // 2, 19)
