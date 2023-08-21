from prettytable import PrettyTable
import itertools as it
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import calendar
import csv

night_games_only = [0,1,2,3,4]
day_games_only = [5,6]


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


class Team:
    def __init__(self, team_name: str, home_game_count: int = 0, away_game_count: int = 0, level: str = ''):
        """

        :param team_name: str
        :param home_game_count: int.  Count of home games in the current tourney
        :param away_game_count: int  Count of away games in the current tourney
        :param level: str  The level of the team
        """
        self.team_name = team_name
        self.level = level
        #self.game_count = self.home_game_count + self.away_game_count
        self.home_game_count = home_game_count
        self.away_game_count = away_game_count


    def __str__(self):
        if not self.level:
            return f'{self.team_name}'
        else:
            return f'{self.level} - {self.team_name}'



def trim_sched(games):
    """
    Remove all Games from list that violate day or night game rule
    :param games:
    :return: games
    """
    print(f'Original List: ')
    for game in games:
        print(game)
    for game in games:
        day_of_week = parse(game.gameday).weekday()
        if day_of_week in day_games_only and game.time_slot == 'Night':
            games.remove(game)
    print(f'Removed Night games from Day Game Days: ')
    for game in games:
        print(game)
    for game in games:
        day_of_week = parse(game.gameday).weekday()
        if day_of_week in night_games_only and game.time_slot != 'Night':
            games.remove(game)
    print(f'Removed Day games from Night Game Days: ')
    for game in games:
        print(game)

    # print(f'Original List: ')
    # for game in games:
    #     print(game)
    # for game in games:
    #     day_of_week = parse(game.gameday).weekday()
    #     if day_of_week in day_games_only and game.time_slot == 'Night':
    #         games.remove(game)
    # print(f'Removed Night games from Day Game Days: ')
    # for game in games:
    #     print(game)
    #     if day_of_week in night_games_only and game.time_slot != 'Night':
    #         games.remove(game)
    # print(f'Removed Day games from Night Game Days: ')
    # for game in games:
    #     print(game)
    return games

def load_data(data_file):
    """
    Load data from CSV file
    :param data_file: csv file
    :return:
    """
    with open(data_file, 'r') as f:
        reader = csv.reader(f)
        data = [item for item in reader]
    return data[0]

def create_teams(teams_list):
    """
    Create list of Team objects from param
    :param teams_list:
    :return: list of Teams
    """
    teams = [Team(team) for team in teams_list]
    return teams


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
    games_list = [Game(game[0],game[2], game[1]) for game in games]
    return games_list


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


def groups_two(teams):
    """
    Return all possible combinations of team pairs
    :type teams: str
    :param teams:
    :return:
    """
    groups = list(it.combinations(teams,2))
    return groups
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


