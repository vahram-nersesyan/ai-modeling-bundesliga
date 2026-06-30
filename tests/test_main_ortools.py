import unittest

from src.model import Match
from src.main_ortools import build_schedule


class FakeSolver:
    """Stand-in for a CP-SAT solver: maps each variable to a fixed value."""

    def __init__(self, values: dict):
        self._values = values

    def value(self, var):
        return self._values[var]


class TestBuildSchedule(unittest.TestCase):

    def test_converts_match_vars_to_match_objects(self):
        match_vars = {
            ("A", "B"): "var_ab",
            ("B", "A"): "var_ba",
        }
        solver = FakeSolver({"var_ab": 1, "var_ba": 4})
        schedule = build_schedule(solver, match_vars)
        self.assertIn(Match("A", "B", 1), schedule)
        self.assertIn(Match("B", "A", 4), schedule)

    def test_one_match_per_var(self):
        match_vars = {
            ("A", "B"): "var_ab",
            ("B", "A"): "var_ba",
        }
        solver = FakeSolver({"var_ab": 1, "var_ba": 4})
        schedule = build_schedule(solver, match_vars)
        self.assertEqual(len(schedule), 2)

    def test_returns_match_instances(self):
        match_vars = {("A", "B"): "var_ab"}
        solver = FakeSolver({"var_ab": 2})
        schedule = build_schedule(solver, match_vars)
        self.assertIsInstance(schedule[0], Match)
