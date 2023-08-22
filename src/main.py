import src.scheduler as s

if __name__ == '__main__':

    # TODO These would go in a config file rather than a data file?

    # Load data
    teams = s.load_data('/Users/Jayco/projects/schedule/data/teams_even.csv')
    time_slots = s.load_data('/Users/Jayco/projects/schedule/data/time_slots.csv')
    fields = s.load_data('/Users/Jayco/projects/schedule/data/fields.csv')
    gamedays = s.load_data('/Users/Jayco/projects/schedule/data/gamedays.csv')
    gamedays = [int(day) for day in gamedays]

    #  TODO better way to intake these params
    tourney_start = '2022-01-01'
    tourney_end = '2022-03-31'
    # Valid days for day and night games.  Monday = 0
    night_games_only = [0, 1, 2, 3, 4]
    day_games_only = [5, 6]
    max_games_per_week = 2
    games_per_team = 20

    # Create list of all possible games
    games = s.create_games(tourney_start, tourney_end, gamedays, fields, time_slots)

    # Trim games to include only valid day-timeslog combinations
    games = s.trim_sched(games, day_games_only, night_games_only)

    # Assign week numbers to trimmed list
    for game in games:
        game.assign_week(tourney_start)

    # Ensure even number of teams
    if len(teams) % 2 == 1:
        teams = teams + 'BYE'

    # Create list of Teams
    teams_list = s.create_teams(teams)

    # Create Matchup pairs
    matches = s.groups_two(teams_list)
    print(5 + 3)
