# Bundesliga CSP – AI Modeling

Work in progress . . .  
Scheduling the Bundesliga season as a Constraint Satisfaction Problem.

**Currently implemented:**
- Variables and Domains Logic: Mapping teams and stadium availability to CSP variables.
- Constraint 1: Season Split: Ensuring every pair plays exactly once in the first half and once in the second half.
- Constraint 2: One Match per Team: Using `AllDifferent` to prevent teams from playing multiple matches simultaneously.
- Constraint 3: Location Validity: Implicitly covered (as every location is tied to a specific home team).
- Constraint 4: Venue Validity: Implicitly covered by variable generation (variables created for both (A,B) at A and (B,A) at B).
- Constraint 5: Sequential Halves: Implicitly covered by strict season split logic (all first-half matches <= split < all second-half matches).

Planned (Next Steps):
- Constraint 6: Mirror Logic: Enforcing the relative order of matches in the second season half.
- Solver & Logging: Exporting valid schedules to `scheduling.log`.

More documentation will follow.