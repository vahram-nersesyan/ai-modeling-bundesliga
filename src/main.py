from constraint import Problem, AllDifferentConstraint

# INPUT
# INPUT - Proof of Concept (6 teams)
# Note: python-constraint doesn't scale well to 18 teams
teams = [
    "Bayern München", "Borussia Dortmund", "RB Leipzig",
    "Bayer Leverkusen", "VfB Stuttgart", "Eintracht Frankfurt"
]

matchdays = list(range(1, 11))  # 10 Spieltage für 6 Teams
location_available = {team: matchdays for team in teams}
season_split = 5  # Hinrunde: 1-5, Rückrunde: 6-10

def generate_variables(problem, teams, location_available):
    """Generate CSP variables for all possible matches."""
    for h in teams:
        for g in teams:
            if h != g:
                problem.addVariable((h, g), location_available[h])


def add_constraints(problem, teams, season_split):
    """Add all scheduling constraints to the CSP problem."""
    
    # Constraint 1: Season Split (each pairing once per half)
    def check_half_season(day1, day2):
        return (day1 <= season_split and day2 > season_split) or \
               (day1 > season_split and day2 <= season_split)
    
    for h in teams:
        for g in teams:
            if h < g:
                problem.addConstraint(check_half_season, [(h, g), (g, h)])
    
    # Constraint 2: One match per team per day
    for h in teams:
        matches = []
        for g in teams:
            if h != g:
                matches.append((h, g))
                matches.append((g, h))
        problem.addConstraint(AllDifferentConstraint(), matches)
    
    # Constraint 6: Mirror Logic (relative ordering) TEMPORARILY DISABLED (too slow with 18 teams)
    # TODO: Optimize or replace with different approach


def solve_schedule(problem, filename="scheduling.log"):
    """Solve the CSP and save the first solution to a file."""
    solutions = problem.getSolutions()
    print(f"Number of solutions: {len(solutions)}\n")
    
    if solutions:
        with open(filename, "w") as f:
            sorted_schedule = sorted(solutions[0].items(), key=lambda x: x[1])
            f.write("-------- Bundesliga scheduling solution --------\n")
            for match, day in sorted_schedule:
                home_team, guest_team = match
                f.write(f"Day {day}: {home_team} vs {guest_team} (at {home_team})\n")
            f.write("------------------------------------\n")
        print(f"Successfully saved schedule to {filename}")
    else:
        print("No solution found!")


# Main execution
if __name__ == "__main__":
    problem = Problem()
    generate_variables(problem, teams, location_available)
    add_constraints(problem, teams, season_split)
    solve_schedule(problem)