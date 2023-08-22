# Rules for Populating Games with Teams

*Where a rule is articulated in `main.py`, it will be indicated with a `ic` tag*

*NOTE:  It is assumed that `trim_sched()` has been run and that all Games are valid*
* `max_games_per_week` is based on level of team.  
* Teams must play against every team before they can face a team for an additional time
* Teams must alternate between Home and Away each time they face each other
* Each team must have one weekend game per week
* `ic` Assume that a Team's season is determined by total number of games rather than the number of times they must play each 
opponent. `games_per_team`
* All leagues must be scheduled at the same time
* Juniors and Intermediate play half their games at other league's fields
* We do not schedule those games, and we do not create schedules for other leagues' teams
* 