from dataclasses import dataclass
from collections import Counter

from src.model import Match


@dataclass
class ValidationResult:
    name: str
    passed: bool
    message: str


def validate_match_count(schedule: list[Match], num_teams: int) -> ValidationResult:
    expected = num_teams * (num_teams - 1)
    actual = len(schedule)
    passed = actual == expected
    message = f"Expected {expected} matches, got {actual}"
    return ValidationResult("match_count", passed, message)


def validate_matches_per_matchday(schedule: list[Match], num_teams: int) -> ValidationResult:
    matches_per_day = Counter(m.day for m in schedule)
    expected_per_day = num_teams // 2
    bad_days = {day: count for day, count in matches_per_day.items() if count != expected_per_day}
    if bad_days:
        return ValidationResult(
            "matches_per_matchday", False,
            f"Expected {expected_per_day} matches per day, violations: {bad_days}",
        )
    return ValidationResult("matches_per_matchday", True, f"All matchdays have {expected_per_day} matches")


def validate_one_match_per_team_per_day(schedule: list[Match]) -> ValidationResult:
    # Count appearances of each (team, day) across both home and away roles.
    appearances = Counter()
    for m in schedule:
        appearances[(m.home, m.day)] += 1
        appearances[(m.away, m.day)] += 1
    bad = {key: count for key, count in appearances.items() if count > 1}
    if bad:
        return ValidationResult(
            "one_match_per_team_per_day", False,
            f"Teams playing more than once on a day: {bad}",
        )
    return ValidationResult(
        "one_match_per_team_per_day", True, "No team plays more than once per day"
    )


def validate_season_split(schedule: list[Match], season_split: int) -> ValidationResult:
    # For each unordered pairing, exactly one leg in the first half, one in the second.
    halves = {}  # frozenset({A, B}) -> [first_half_count, second_half_count]
    for m in schedule:
        pairing = frozenset({m.home, m.away})
        counts = halves.setdefault(pairing, [0, 0])
        if m.day <= season_split:
            counts[0] += 1
        else:
            counts[1] += 1
    bad = {
        tuple(sorted(pairing)): counts
        for pairing, counts in halves.items()
        if counts != [1, 1]
    }
    if bad:
        return ValidationResult(
            "season_split", False,
            f"Pairings not split one-per-half [first, second]: {bad}",
        )
    return ValidationResult(
        "season_split", True, "Every pairing plays once per half"
    )


def validate_home_away_pairing(schedule: list[Match]) -> ValidationResult:
    # Each unordered pairing must have exactly one match at each team's home.
    legs = {}  # frozenset({A, B}) -> list of home teams
    for m in schedule:
        pairing = frozenset({m.home, m.away})
        legs.setdefault(pairing, []).append(m.home)
    bad = {
        tuple(sorted(pairing)): sorted(homes)
        for pairing, homes in legs.items()
        if sorted(homes) != sorted(pairing)
    }
    if bad:
        return ValidationResult(
            "home_away_pairing", False,
            f"Pairings without exactly one home each {{pairing: home teams}}: {bad}",
        )
    return ValidationResult(
        "home_away_pairing", True, "Every pairing has one home and one away leg"
    )


def validate(schedule: list[Match], num_teams: int, season_split: int) -> list[ValidationResult]:
    # Run every validation check and collect the results.
    return [
        validate_match_count(schedule, num_teams),
        validate_matches_per_matchday(schedule, num_teams),
        validate_one_match_per_team_per_day(schedule),
        validate_season_split(schedule, season_split),
        validate_home_away_pairing(schedule),
    ]
