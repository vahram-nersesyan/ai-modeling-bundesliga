import unittest

from src.model import Match
from src.validator import validate_match_count, validate_matches_per_matchday


def make_schedule(num_teams: int) -> list[Match]:
    """Build a valid round-robin schedule for num_teams teams."""
    teams = [f"Team{i}" for i in range(num_teams)]
    num_matchdays = (num_teams - 1) * 2
    matches_per_day = num_teams // 2
    schedule = []
    match_list = []
    for i, home in enumerate(teams):
        for j, away in enumerate(teams):
            if i != j:
                match_list.append((home, away))
    day = 1
    count = 0
    for home, away in match_list:
        schedule.append(Match(home=home, away=away, day=day))
        count += 1
        if count == matches_per_day:
            day += 1
            count = 0
    return schedule


class TestValidateMatchCount(unittest.TestCase):

    def test_valid_4_teams(self):
        schedule = make_schedule(4)
        result = validate_match_count(schedule, num_teams=4)
        self.assertTrue(result.passed)

    def test_valid_18_teams(self):
        schedule = make_schedule(18)
        result = validate_match_count(schedule, num_teams=18)
        self.assertTrue(result.passed)

    def test_too_few_matches(self):
        schedule = make_schedule(4)[:5]
        result = validate_match_count(schedule, num_teams=4)
        self.assertFalse(result.passed)
        self.assertIn("Expected 12", result.message)
        self.assertIn("got 5", result.message)

    def test_too_many_matches(self):
        schedule = make_schedule(4) + [Match(home="TeamX", away="TeamY", day=1)]
        result = validate_match_count(schedule, num_teams=4)
        self.assertFalse(result.passed)

    def test_result_has_name(self):
        schedule = make_schedule(4)
        result = validate_match_count(schedule, num_teams=4)
        self.assertEqual(result.name, "match_count")


class TestValidateMatchesPerMatchday(unittest.TestCase):

    def test_valid_4_teams(self):
        schedule = make_schedule(4)
        result = validate_matches_per_matchday(schedule, num_teams=4)
        self.assertTrue(result.passed)

    def test_uneven_day_fails(self):
        schedule = [
            Match(home="A", away="B", day=1),
            Match(home="C", away="D", day=1),
            Match(home="A", away="C", day=1),  # 3 matches on day 1
            Match(home="B", away="D", day=2),
            Match(home="A", away="D", day=2),
        ]
        result = validate_matches_per_matchday(schedule, num_teams=4)
        self.assertFalse(result.passed)
        self.assertIn("violations", result.message)

    def test_result_has_name(self):
        schedule = make_schedule(4)
        result = validate_matches_per_matchday(schedule, num_teams=4)
        self.assertEqual(result.name, "matches_per_matchday")
