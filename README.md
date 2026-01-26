# Bundesliga Schedule Generator

Generating valid Bundesliga season schedules using Constraint Satisfaction Programming.

## The Problem
Schedule 306 matches (18 teams × 17 opponents × 2 legs) across 34 matchdays while satisfying:
- Each team plays exactly once per matchday
- Each pairing plays once in first half (Hinrunde), once in second half (Rückrunde)
- Home/away venue constraints

## Technical Journey
Started with `python-constraint` – worked for 4-6 teams but didn't scale. Systematic benchmarking showed exponential blowup, leading to migration to **Google OR-Tools CP-SAT solver**.

| Teams | python-constraint | OR-Tools |
|-------|-------------------|----------|
| 4     | <1s               | <1s      |
| 6     | ~2s               | <1s      |
| 18    | ∞ (timeout)       | TBD      |

## Status
OR-Tools migration in progress – core constraints implemented, logging next.