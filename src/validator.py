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
