import scheduler as s

if __name__ == '__main__':
    teams = s.load_data('/Users/Jayco/projects/schedule/data/teams_even.csv')
    time_slots = s.load_data('/Users/Jayco/projects/schedule/data/time_slots.csv')
    fields = s.load_data('/Users/Jayco/projects/schedule/data/fields.csv')
    gamedays = s.load_data('/Users/Jayco/projects/schedule/data/gamedays.csv')
    gamedays = [int(day) for day in gamedays]

    #  TODO better way to intake these params
    tourney_start = '2022-01-01'
    tourney_end = '2022-03-31'

    games = s.create_games(tourney_start, tourney_end, gamedays, fields, time_slots)
    for game in games:
        game.assign_week(tourney_start)
    matches = s.groups_two(teams)
    print(5 + 3)
