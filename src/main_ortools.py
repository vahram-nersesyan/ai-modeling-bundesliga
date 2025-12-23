"""
Bundesliga Schedule Generator using Google OR-Tools CP-SAT Solver
Migrated from python-constraint for better performance and scalability
"""

from ortools.sat.python import cp_model

# ============================================================================
# CONFIGURATION
# ============================================================================

# 18 Bundesliga teams (2025/26 season)
TEAMS = [
    "Bayern München", "Bayer Leverkusen", "Eintracht Frankfurt", "Borussia Dortmund",
    "SC Freiburg", "Mainz 05", "RB Leipzig", "Werder Bremen",
    "VfB Stuttgart", "Borussia Mönchengladbach", "VfL Wolfsburg", "FC Augsburg",
    "Union Berlin", "FC St. Pauli", "TSG Hoffenheim", "1. FC Heidenheim",
    "1. FC Köln", "Hamburger SV"
]


NUM_TEAMS = len(TEAMS)
NUM_MATCHDAYS = (NUM_TEAMS - 1) * 2  # 34 matchdays for 18 teams
SEASON_SPLIT = NUM_MATCHDAYS // 2    # Day 17 splits first and second half of season


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