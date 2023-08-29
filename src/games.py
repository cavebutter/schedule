import datetime
import itertools as it
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from src.teams import Team


class Game:
    def __init__(self, field, time_slot, gameday):
        self.field = field
        self.time_slot = time_slot
        self.gameday = gameday
        self.hometeam = None
        self.awayteam = None
        self.week_no = 0

    def __str__(self):
        return f'{self.gameday} - {self.time_slot} - {self.field}'

    def assign_week(self, start_date):
        """
        Assigns the week number based on the start date.

        Parameters:
            start_date (str): The start date of the tournament

        Returns:
            None
        """
        gameday = parse(self.gameday)
        start = parse(start_date)
        week_no = relativedelta(gameday, start).weeks
        self.week_no = week_no

    def assign_teams_to_game(self, match: tuple):
        """
        Assign the first Team in the match tuple to the Home team in the Game.  Assign the second Team to Away.
        :param match:
        """
        if not isinstance(match[0], Team) and isinstance(match[1], Team):
            raise ValueError("Both elements of 'match' must be instances of the 'Team' class")
        self.hometeam = match[0]
        self.awayteam = match[1]
        self.hometeam.increment_home_count()
        self.awayteam.increment_away_count()


def trim_sched(games:list, day_games:list, night_games:list):
    """
    Remove all Games from list that violate day or night game rule
    :param games:
    :return: games
    """
    for game in games:
        day_of_week = parse(game.gameday).weekday()
        if day_of_week in day_games and game.time_slot == 'Night':
            games.remove(game)
        elif day_of_week in night_games and game.time_slot != 'Night':
            games.remove(game)
    return games


def create_games(start_date, end_date, gamedays, fields, time_slots):
    """
    Return a list of Games based on passed parameters.
    :type start_date: str
    :type end_date: str
    :type gamedays: list
    :type fields: list
    :type time_slots: list
    :param start_date:
    :param end_date:
    :param gamedays:
    :param fields:
    :param time_slots:
    :return: list of Game objects
    """
    if not isinstance(start_date, str):
        raise TypeError('start_date must be a string.')
    if not isinstance(end_date, str):
        raise TypeError('end_date must be a string.')
    if not isinstance(gamedays, list):
        raise TypeError('gamedays must be a list.')
    if not isinstance(fields, list):
        raise TypeError('fields must be a list.')
    if not isinstance(time_slots, list):
        raise TypeError('time_slots must be a list.')

    dates = eligible_game_days(start_date, end_date, gamedays)
    games = list(it.product(fields, dates, time_slots))
    games_list = [Game(game[0], game[2], game[1]) for game in games]
    return games_list


def eligible_game_days(tournament_start, tournament_end, game_days):
    """
    Given tournament start and end dates, return a list of game days as strings that fall between
    the two.
    :type game_days: list
    :type tournament_end: string
    :type tournament_start: string
    :param tournament_start:
    :param tournament_end:
    :param game_days:
    :return: list of date strings
    """
    tournament_start = datetime.datetime.strptime(tournament_start, "%Y-%m-%d")
    tournament_end = datetime.datetime.strptime(tournament_end, "%Y-%m-%d")
    if tournament_start > tournament_end:
        raise ValueError('Tournament start date must be before tournament end date.')
    if not isinstance(game_days, list):
        raise TypeError('game_days must be a list.')
    for day in game_days:
        if not isinstance(day, int) or day < 0 or day > 6:
            raise ValueError('game_days must be a list of integers between 0 and 6.')
    days = []
    while tournament_start <= tournament_end:
        if tournament_start.weekday() in game_days:
            days.append(tournament_start.strftime("%a %b %d, %Y"))
        tournament_start = tournament_start + datetime.timedelta(days=1)
    return days
