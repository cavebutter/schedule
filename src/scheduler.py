from prettytable import PrettyTable
import itertools
import datetime
import calendar


class Game:
    def __init__(self, field, time_slot, gameday):
        self.field = field
        self.time_slot = time_slot
        self.gameday = gameday
        self.hometeam = None
        self.awayteam = None

    def __str__(self):
        return f'{self.gameday} - {self.field}'

def groups(teams):
    """
    Create 2 equal sized groups of teams from a single list of teams.
    :type teams: list
    :param teams:
    :return: dict containing 2 lists
    """
    if not isinstance(teams, list):
        raise TypeError('teams must be a list.')
    if len(teams) % 2 == 1:
        teams.append('BYE')
    mid = int(len(teams)//2)
    l1, l2 = teams[:mid], teams[mid:]
    grouped_teams = {'group1': l1, 'group2': l2}
    return grouped_teams


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

def create_schedule(teams, time_slots, fields, tournament_start, tournament_end, game_days, ngames):
    """
    Generate a round-robin style schedule based on passed params.
    :type ngames: int
    :type game_days: int
    :type tournament_end: datetime
    :type tournament_start: datetime
    :type fields: list
    :type time_slots: list
    :type teams: list
    :param teams: List of teams participating in tournament
    :param time_slots: Names of the timeslots for each game (e.g. Early, Late)
    :param fields: Names of the fields available for use in the tournament
    :param tournament_start: Calendar date for the start of the tournament.  Constrained by game_days
    :param tournament_end: Calendar date for the end of the tournament.  Constrained by game_days
    :param game_days: Numberical representation of days of the week eligible to play games.  Monday = 0
    :param ngames: Number of games each time must play in the tournament
    :return: TBD
    """
    pass


