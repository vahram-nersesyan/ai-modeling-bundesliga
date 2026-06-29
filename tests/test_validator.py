import unittest

from src.model import Match
from src.validator import (
    validate_match_count,
    validate_matches_per_matchday,
    validate_one_match_per_team_per_day,
    validate_season_split,
    validate_home_away_pairing,
    validate,
)


# A valid 4-team double round-robin: 12 matches across 6 days, 2 per day.
# Days 1-3 are the first half, days 4-6 the second half (season_split = 3).
# Every team plays once per day; every pairing plays once per half.
VALID_4_TEAM_SCHEDULE = [
    Match("A", "B", 1), Match("C", "D", 1),
    Match("A", "C", 2), Match("D", "B", 2),
    Match("A", "D", 3), Match("B", "C", 3),
    Match("B", "A", 4), Match("D", "C", 4),
    Match("C", "A", 5), Match("B", "D", 5),
    Match("D", "A", 6), Match("C", "B", 6),
]


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


class TestValidateOneMatchPerTeamPerDay(unittest.TestCase):

    def test_valid_schedule_passes(self):
        result = validate_one_match_per_team_per_day(VALID_4_TEAM_SCHEDULE)
        self.assertTrue(result.passed)

    def test_team_twice_as_home_fails(self):
        schedule = [
            Match("A", "B", 1),
            Match("A", "C", 1),  # A plays twice on day 1
        ]
        result = validate_one_match_per_team_per_day(schedule)
        self.assertFalse(result.passed)

    def test_team_once_home_once_away_same_day_fails(self):
        schedule = [
            Match("A", "B", 1),
            Match("C", "A", 1),  # A is home then away on day 1
        ]
        result = validate_one_match_per_team_per_day(schedule)
        self.assertFalse(result.passed)

    def test_same_pairing_different_days_passes(self):
        schedule = [
            Match("A", "B", 1),
            Match("B", "A", 2),
        ]
        result = validate_one_match_per_team_per_day(schedule)
        self.assertTrue(result.passed)

    def test_result_has_name(self):
        result = validate_one_match_per_team_per_day(VALID_4_TEAM_SCHEDULE)
        self.assertEqual(result.name, "one_match_per_team_per_day")


class TestValidateSeasonSplit(unittest.TestCase):

    def test_valid_schedule_passes(self):
        result = validate_season_split(VALID_4_TEAM_SCHEDULE, season_split=3)
        self.assertTrue(result.passed)

    def test_both_legs_in_first_half_fails(self):
        schedule = [
            Match("A", "B", 1),
            Match("B", "A", 2),  # both legs in first half (split=3)
        ]
        result = validate_season_split(schedule, season_split=3)
        self.assertFalse(result.passed)

    def test_both_legs_in_second_half_fails(self):
        schedule = [
            Match("A", "B", 4),
            Match("B", "A", 5),  # both legs in second half (split=3)
        ]
        result = validate_season_split(schedule, season_split=3)
        self.assertFalse(result.passed)

    def test_one_leg_per_half_passes(self):
        schedule = [
            Match("A", "B", 1),
            Match("B", "A", 4),
        ]
        result = validate_season_split(schedule, season_split=3)
        self.assertTrue(result.passed)

    def test_result_has_name(self):
        result = validate_season_split(VALID_4_TEAM_SCHEDULE, season_split=3)
        self.assertEqual(result.name, "season_split")


class TestValidateHomeAwayPairing(unittest.TestCase):

    def test_valid_schedule_passes(self):
        result = validate_home_away_pairing(VALID_4_TEAM_SCHEDULE)
        self.assertTrue(result.passed)

    def test_both_legs_same_home_fails(self):
        schedule = [
            Match("A", "B", 1),
            Match("A", "B", 4),  # A is home both times
        ]
        result = validate_home_away_pairing(schedule)
        self.assertFalse(result.passed)

    def test_one_home_each_passes(self):
        schedule = [
            Match("A", "B", 1),
            Match("B", "A", 4),
        ]
        result = validate_home_away_pairing(schedule)
        self.assertTrue(result.passed)

    def test_result_has_name(self):
        result = validate_home_away_pairing(VALID_4_TEAM_SCHEDULE)
        self.assertEqual(result.name, "home_away_pairing")


class TestValidate(unittest.TestCase):

    def test_valid_schedule_all_pass(self):
        results = validate(VALID_4_TEAM_SCHEDULE, num_teams=4, season_split=3)
        self.assertTrue(all(r.passed for r in results))

    def test_returns_one_result_per_check(self):
        results = validate(VALID_4_TEAM_SCHEDULE, num_teams=4, season_split=3)
        self.assertEqual(len(results), 5)

    def test_broken_schedule_reports_failures(self):
        # A plays twice on day 1; also breaks home/away and season split.
        broken = [Match("A", "B", 1), Match("A", "B", 1)]
        results = validate(broken, num_teams=4, season_split=3)
        failed = [r.name for r in results if not r.passed]
        self.assertIn("one_match_per_team_per_day", failed)
        self.assertIn("home_away_pairing", failed)

    def test_each_result_names_unique(self):
        results = validate(VALID_4_TEAM_SCHEDULE, num_teams=4, season_split=3)
        names = [r.name for r in results]
        self.assertEqual(len(names), len(set(names)))
