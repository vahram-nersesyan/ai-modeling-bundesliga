from constraint import Problem, AllDifferentConstraint

# INPUT
teams = ["A", "B", "C", "D"]
location_available = {
    "A": [1, 4, 6, 7, 8, 10],
    "B": [2, 4, 5, 6, 7, 9],
    "C": [2, 3, 5, 8, 10],
    "D": [1, 3, 6, 8, 9, 10],
}
season_split = 5  # Will be 17 for real Bundesliga


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
    
    # Constraint 6: Mirror Logic (relative ordering)
    def mirror_logic(home1, away1, home2, away2):
        leg1_pair1 = min(home1, away1)
        leg2_pair1 = max(home1, away1)
        leg1_pair2 = min(home2, away2)
        leg2_pair2 = max(home2, away2)
        
        if leg1_pair1 <= leg1_pair2 and leg2_pair1 <= leg2_pair2:
            return True
        if leg1_pair1 >= leg1_pair2 and leg2_pair1 >= leg2_pair2:
            return True
        return False
    
    pairings = []
    for h in teams:
        for g in teams:
            if h < g:
                pairings.append((h, g))
    
    for i in range(len(pairings)):
        for j in range(i + 1, len(pairings)):
            pair1 = pairings[i]
            pair2 = pairings[j]
            pair1_away = (pair1[1], pair1[0])
            pair2_away = (pair2[1], pair2[0])
            problem.addConstraint(mirror_logic, [pair1, pair1_away, pair2, pair2_away])


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