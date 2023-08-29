import pytest

import src.games
import src.teams as sched
import datetime

#  FIXTURES
@pytest.fixture
def even_teams():
    teams = ['Dodgers', 'Rays', 'Rangers', 'Mariners', 'Reds', 'Yankees']
    return teams

@pytest.fixture
def two_time_slots():
    time_slots = ['Early', 'Late']
    return time_slots

@pytest.fixture
def fields():
    fields = ['Field_1', 'Field_2']
    return fields

@pytest.fixture
def tourney_start():
    tournament_start = 'May 1, 2023'
    return tournament_start

@pytest.fixture
def tourney_end():
    tournament_end = 'June 1, 2023'
    return tournament_end

@pytest.fixture
def gamedays():
    game_days = [0, 5]  # days of week. Monday == 0
    return game_days

@pytest.fixture
def ngames():
    ngames = 20
    return ngames


#  TESTS
def test_gamedays(tourney_start, tourney_end, gamedays):
    days = src.games.eligible_game_days(tourney_start, tourney_end, gamedays)
    days = days
    assert days == ['Sat Mar 04, 2023', 'Mon Mar 06, 2023', 'Sat Mar 11, 2023',
                    'Mon Mar 13, 2023', 'Sat Mar 18, 2023', 'Mon Mar 20, 2023',
                    'Sat Mar 25, 2023', 'Mon Mar 27, 2023', 'Sat Apr 01, 2023']


# Generated by CodiumAI

import pytest

#  Tests that the function returns the correct list of game days when the tournament start and end dates are exactly one month apart and game_days is [0, 2, 4]
def test_week_apart_game_days_1(self):
    start_date = '2022-01-01'
    end_date = '2022-02-01'
    game_days = [0, 2, 4]
    expected_result = ['Sat Jan 01, 2022', 'Mon Jan 03, 2022', 'Wed Jan 05, 2022', 'Fri Jan 07, 2022', 'Sun Jan 09, 2022', 'Tue Jan 11, 2022', 'Thu Jan 13, 2022', 'Sat Jan 15, 2022', 'Mon Jan 17, 2022', 'Wed Jan 19, 2022', 'Fri Jan 21, 2022', 'Sun Jan 23, 2022', 'Tue Jan 25, 2022', 'Thu Jan 27, 2022', 'Sat Jan 29, 2022', 'Tue Jan 01, 2022']
    assert src.games.eligible_game_days(start_date, end_date, game_days) == expected_result

#  Tests that the function returns the correct list of game days when the tournament start and end dates are the same and game_days is [0, 2, 4]
def test_same_day_game_days_1(self):
    start_date = '2022-01-01'
    end_date = '2022-01-01'
    game_days = [0, 2, 4]
    expected_result = ['Sat Jan 01, 2022']
    assert src.games.eligible_game_days(start_date, end_date, game_days) == expected_result

#  Tests that the function returns the correct list of game days when the tournament start and end dates are the same and game_days is [1, 3, 5]
def test_same_day_game_days_2(self):
    start_date = '2022-01-01'
    end_date = '2022-01-01'
    game_days = [1, 3, 5]
    expected_result = []
    assert src.games.eligible_game_days(start_date, end_date, game_days) == expected_result
