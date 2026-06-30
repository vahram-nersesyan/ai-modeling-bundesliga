"""
Bundesliga Schedule Generator using Google OR-Tools CP-SAT Solver
Migrated from python-constraint for better performance and scalability
"""

from ortools.sat.python import cp_model
from src.config import TEAMS, NUM_TEAMS, NUM_MATCHDAYS, SEASON_SPLIT
from src.model import Match
from src.validator import validate


# ============================================================================
# MODEL SETUP
# ============================================================================

def create_model():
    """
    Creates the CP-SAT model with all variables and constraints.
    Returns: (model, match_vars) where match_vars is a dict mapping (home, away) -> IntVar
    """
    model = cp_model.CpModel()
    match_vars = {}
    
    # ========================================================================
    # VARIABLES: Create a variable for each possible match
    # ========================================================================
    # For each pair of teams (home, away), we create an integer variable
    # representing the matchday when this match is played (1 to 34)
    
    for i, home in enumerate(TEAMS):
        for j, away in enumerate(TEAMS):
            if i != j:  # A team can't play itself
                var_name = f"{home}_vs_{away}"
                # Each match happens on a day between 1 and NUM_MATCHDAYS
                match_vars[(home, away)] = model.NewIntVar(
                    1, NUM_MATCHDAYS, var_name
                )

    # ========================================================================
    # CONSTRAINT 1: Season Split (Hinrunde/Rückrunde)
    # ========================================================================
    # Each pairing {A, B} must play once in first half (days 1-17)
    # and once in second half (days 18-34)
    
    for i, team_a in enumerate(TEAMS):
        for j, team_b in enumerate(TEAMS):
            if i < j:  # Only check each pairing once
                match_ab = match_vars[(team_a, team_b)]  # A vs B at A's home
                match_ba = match_vars[(team_b, team_a)]  # B vs A at B's home
                
                # One match in first half, one in second half
                # Create boolean variables to track which half each match is in
                ab_first_half = model.NewBoolVar(f"{team_a}_{team_b}_first")
                ba_first_half = model.NewBoolVar(f"{team_b}_{team_a}_first")
                
                # ab_first_half is True iff match_ab <= SEASON_SPLIT
                model.Add(match_ab <= SEASON_SPLIT).OnlyEnforceIf(ab_first_half)
                model.Add(match_ab > SEASON_SPLIT).OnlyEnforceIf(ab_first_half.Not())
                
                # ba_first_half is True iff match_ba <= SEASON_SPLIT
                model.Add(match_ba <= SEASON_SPLIT).OnlyEnforceIf(ba_first_half)
                model.Add(match_ba > SEASON_SPLIT).OnlyEnforceIf(ba_first_half.Not())
                
                # Exactly one of them must be in first half (XOR)
                model.Add(ab_first_half + ba_first_half == 1)

    # ========================================================================
    # CONSTRAINT 2: One Match Per Team Per Day
    # ========================================================================
    # A team can only play one match on any given day
    
    for team in TEAMS:
        for day in range(1, NUM_MATCHDAYS + 1):
            # Collect all matches involving this team on this day
            matches_on_day = []
            
            for opponent in TEAMS:
                if opponent != team:
                    # Home match: team vs opponent
                    home_match = match_vars[(team, opponent)]
                    is_home_match = model.NewBoolVar(f"{team}_home_{opponent}_day{day}")
                    model.Add(home_match == day).OnlyEnforceIf(is_home_match)
                    model.Add(home_match != day).OnlyEnforceIf(is_home_match.Not())
                    matches_on_day.append(is_home_match)
                    
                    # Away match: opponent vs team
                    away_match = match_vars[(opponent, team)]
                    is_away_match = model.NewBoolVar(f"{team}_away_{opponent}_day{day}")
                    model.Add(away_match == day).OnlyEnforceIf(is_away_match)
                    model.Add(away_match != day).OnlyEnforceIf(is_away_match.Not())
                    matches_on_day.append(is_away_match)
            
            # At most 1 match per team per day
            model.Add(sum(matches_on_day) <= 1)
    
    return model, match_vars

# ========================================================================
# Solution
# ========================================================================

def solve(model):
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        return solver
    else:
        print("No solution was found!")
    
def build_schedule(solver, match_vars) -> list[Match]:
    # Convert the solver's assignment into a list of Match objects.
    schedule = []
    for (home, away), var in match_vars.items():
        schedule.append(Match(home=home, away=away, day=solver.value(var)))
    return schedule


def print_schedule(schedule: list[Match]) -> None:
    # Print the schedule sorted by matchday.
    for m in sorted(schedule, key=lambda m: m.day):
        print(f"Day {m.day}: {m.home} vs {m.away}")


def print_validation(schedule: list[Match]) -> None:
    # Run all validators on the schedule and print each result.
    results = validate(schedule, num_teams=NUM_TEAMS, season_split=SEASON_SPLIT)
    print("\n--- Validation ---")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"[{status}] {r.name}: {r.message}")

if __name__ == "__main__":
    model, match_vars = create_model()
    solver = solve(model)
    if solver:
        schedule = build_schedule(solver, match_vars)
        print_schedule(schedule)
        print_validation(schedule)