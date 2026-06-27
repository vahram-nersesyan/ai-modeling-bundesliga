import unittest

from src.model import Match


class TestMatch(unittest.TestCase):

    def test_fields(self):
        m = Match(home="Bayern München", away="Borussia Dortmund", day=1)
        self.assertEqual(m.home, "Bayern München")
        self.assertEqual(m.away, "Borussia Dortmund")
        self.assertEqual(m.day, 1)

    def test_equality(self):
        a = Match(home="Bayern München", away="Borussia Dortmund", day=1)
        b = Match(home="Bayern München", away="Borussia Dortmund", day=1)
        self.assertEqual(a, b)

    def test_inequality_different_day(self):
        a = Match(home="Bayern München", away="Borussia Dortmund", day=1)
        b = Match(home="Bayern München", away="Borussia Dortmund", day=2)
        self.assertNotEqual(a, b)

    def test_inequality_swapped_teams(self):
        a = Match(home="Bayern München", away="Borussia Dortmund", day=1)
        b = Match(home="Borussia Dortmund", away="Bayern München", day=1)
        self.assertNotEqual(a, b)

    def test_is_immutable(self):
        m = Match(home="Bayern München", away="Borussia Dortmund", day=1)
        with self.assertRaises(AttributeError):
            m.day = 5

    def test_usable_in_set(self):
        a = Match(home="Bayern München", away="Borussia Dortmund", day=1)
        b = Match(home="Bayern München", away="Borussia Dortmund", day=1)
        self.assertEqual(len({a, b}), 1)
