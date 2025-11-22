# Bundesliga CSP – AI Modeling

Work in progress . . .  
Scheduling the Bundesliga season as a Constraint Satisfaction Problem.

Currently implemented:
- Variables and Domains Logic: Mapping teams and stadium availability to CSP variables.
- Constraint: Season Split: Ensuring every pair plays exactly once in the first half and once in the second half.
- Constraint: One Match per Team: Using `AllDifferent` to prevent teams from playing multiple matches simultaneously.
- Constraint: Location Validity: Implicitly covered (as every location is tied to a specific home team).

Planned (Next Steps):
- Constraint: Home/Away Balance: Ensuring alternating home and away matches.
- Constraint: Mirror Logic: Enforcing the relative order of matches in the second season half.
- Solver & Logging: Exporting valid schedules to `scheduling.log`.

More documentation will follow.