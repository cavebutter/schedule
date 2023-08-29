from src.games import *


class TestEligibleGameDays:

    #  Tests that the function returns the correct list of game days when the tournament start and end dates are exactly one week apart and the game_days list contains all days of the week.
    def test_tournament_one_week_all_days(self):
        # Arrange
        tournament_start = "2022-01-01"
        tournament_end = "2022-01-07"
        game_days = [0, 1, 2, 3, 4, 5, 6]

        # Act
        result = eligible_game_days(tournament_start, tournament_end, game_days)

        # Assert
        assert result == ["Sat Jan 01, 2022", "Sun Jan 02, 2022", "Mon Jan 03, 2022", "Tue Jan 04, 2022",
                          "Wed Jan 05, 2022", "Thu Jan 06, 2022", "Fri Jan 07, 2022"]

    def test_tournament_one_week_one_day(self):
        # Arrange
        tournament_start = "2022-01-01"
        tournament_end = "2022-01-07"
        game_days = [0]

        # Act
        result = eligible_game_days(tournament_start, tournament_end, game_days)

        # Assert
        assert result == ["Mon Jan 03, 2022"]

    def test_tournament_one_week_multiple_days(self):
        # Arrange
        tournament_start = "2023-01-01"
        tournament_end = "2023-01-07"
        game_days = [1, 3, 5]

        # Act
        result = eligible_game_days(tournament_start, tournament_end, game_days)

        # Assert
        assert result == ['Tue Jan 03, 2023', 'Thu Jan 05, 2023', 'Sat Jan 07, 2023']

    #  Tests that the function returns the correct list of game days when the tournament start and end dates are more than one week apart and the game_days list contains all days of the week.
    def test_tournament_more_than_one_week_all_days(self):
        # Arrange
        tournament_start = "2022-01-01"
        tournament_end = "2022-01-14"
        game_days = [0, 1, 2, 3, 4, 5, 6]

        # Act
        result = eligible_game_days(tournament_start, tournament_end, game_days)

        # Assert
        assert result == ["Sat Jan 01, 2022", "Sun Jan 02, 2022", "Mon Jan 03, 2022", "Tue Jan 04, 2022",
                          "Wed Jan 05, 2022", "Thu Jan 06, 2022", "Fri Jan 07, 2022", "Sat Jan 08, 2022",
                          "Sun Jan 09, 2022", "Mon Jan 10, 2022", "Tue Jan 11, 2022", "Wed Jan 12, 2022",
                          "Thu Jan 13, 2022", "Fri Jan 14, 2022"]

    #  Tests that the function returns the correct list of game days when the tournament start and end dates are more than one week apart and the game_days list contains only one day of the week.
    def test_tournament_more_than_one_week_one_day(self):
        # Arrange
        tournament_start = "2023-01-01"
        tournament_end = "2023-01-14"
        game_days = [0]

        # Act
        result = eligible_game_days(tournament_start, tournament_end, game_days)

        # Assert
        assert result == ['Mon Jan 02, 2023', 'Mon Jan 09, 2023']


class TestCreateGames:

    #  Tests that the function returns a list of Game objects when valid parameters are passed.
    def test_valid_parameters_returns_list_of_game_objects(self):
        # Arrange
        start_date = "2022-01-01"
        end_date = "2022-01-07"
        gamedays = [0, 1, 2, 3, 4, 5, 6]
        fields = ["Field A", "Field B"]
        time_slots = ["Morning", "Afternoon", "Evening"]

        # Act
        result = create_games(start_date, end_date, gamedays, fields, time_slots)

        # Assert
        assert isinstance(result, list)
        assert all(isinstance(game, Game) for game in result)

    #  Tests that the function returns a list of eligible game days.
    def test_eligible_game_days_returns_empty_list(self):
        # Arrange
        start_date = "2022-01-08"
        end_date = "2022-01-11"
        gamedays = [3]
        fields = ["Field A", "Field B"]
        time_slots = ["Morning", "Afternoon", "Evening"]

        # Act
        result = create_games(start_date, end_date, gamedays, fields, time_slots)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    #  Tests that the function returns a list of Game objects when only one eligible game day is found.
    def test_one_eligible_game_day_returns_list_of_game_objects(self):
        # Arrange
        start_date = "2022-01-01"
        end_date = "2022-01-01"
        gamedays = [0, 1, 2, 3, 4, 5, 6]
        fields = ["Field A", "Field B"]
        time_slots = ["Morning", "Afternoon", "Evening"]

        # Act
        result = create_games(start_date, end_date, gamedays, fields, time_slots)

        # Assert
        assert isinstance(result, list)
        assert all(isinstance(game, Game) for game in result)


class TestAssignWeek:

    #  Tests that the week number is assigned correctly when the start date is before the game day
    def test_assign_week_start_before_game_day(self):
        # Arrange
        start_date = "2022-01-01"
        game = Game("Field A", "10:00", "2022-01-10")

        # Act
        game.assign_week(start_date)

        # Assert
        assert game.week_no == 1

    #  Tests that the week number is assigned correctly when the start date is the same as the game day
    def test_assign_week_start_same_as_game_day(self):
        # Arrange
        start_date = "2022-01-10"
        game = Game("Field A", "10:00", "2022-01-10")

        # Act
        game.assign_week(start_date)

        # Assert
        assert game.week_no == 0

    #  Tests that the week number is assigned correctly when the start date is after the game day
    def test_assign_week_start_after_game_day(self):
        # Arrange
        start_date = "2022-01-20"
        game = Game("Field A", "10:00", "2022-01-10")

        # Act
        game.assign_week(start_date)

        # Assert
        assert game.week_no == -1

    #  Tests that the week number is assigned correctly when the start date is in a leap year
    def test_assign_week_leap_year(self):
        # Arrange
        start_date = "2020-01-01"
        game = Game("Field A", "10:00", "2020-01-10")

        # Act
        game.assign_week(start_date)

        # Assert
        assert game.week_no == 1

    #  Tests that the week number is assigned correctly when the start date is in a non-leap year
    def test_assign_week_non_leap_year(self):
        # Arrange
        start_date = "2021-01-01"
        game = Game("Field A", "10:00", "2021-01-10")

        # Act
        game.assign_week(start_date)

        # Assert
        assert game.week_no == 1


class TestTrimSched:

    #  Tests that the function correctly removes games with invalid timeslots for their day of the week
    def test_all_day_games(self):
        # Arrange
        night_games_only = [0, 1, 2, 3, 4]
        day_games_only = [5, 6]
        games = [
            Game(gameday='2021-01-02', time_slot='Day', field='Field A'), # Saturday - Should remain
            Game(gameday='2021-01-03', time_slot='Night', field='Field A'), # Sunday - Should remove night game on Sunaay
            Game(gameday='2021-01-04', time_slot='Night', field='Field A'),  # Monday - Should remain
            Game(gameday='2021-01-05', time_slot='Night', field='Field A'),  # Tuesday - Should remain
            Game(gameday='2021-01-06', time_slot='Day', field='Field A'),  # Wednesday - Should remove day game on Wed
        ]

        # Act
        results = trim_sched(games, day_games_only, night_games_only)
        res_gamedays = [result.gameday for result in results]

        # Assert
        expected_result = ['2021-01-02','2021-01-04','2021-01-05']
        assert res_gamedays == expected_result
