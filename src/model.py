from dataclasses import dataclass


@dataclass(frozen=True)
class Match:
    home: str
    away: str
    day: int
