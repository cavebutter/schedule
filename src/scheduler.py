import os
import itertools as it
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import csv
import os.path

night_games_only = [0,1,2,3,4]
day_games_only = [5,6]
games_per_team = 20


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


class Team:
    def __init__(self, team_name: str, level: str, home_game_count: int = 0, away_game_count: int = 0):
        """

        :param team_name: str
        :param home_game_count: int.  Count of home games in the current tourney
        :param away_game_count: int  Count of away games in the current tourney
        :param level: str  The level of the team
        """
        if not team_name:
            raise ValueError("team_name cannot be an empty string")
        if not level:
            raise ValueError('level cannot be an empty string')
        self.team_name = team_name
        self.level = level
        self.home_game_count = home_game_count
        self.away_game_count = away_game_count

    def __str__(self):
        if self.level =='':
            return f'{self.team_name}'
        else:
            return f'{self.level} - {self.team_name}'

    def increment_home_count(self):
        """
        Increments the home_game_count by 1.
        :return:
        """
        self.home_game_count += 1

    def increment_away_count(self):
        """
        Increments the home_game_count by 1.
        :return:
        """
        self.away_game_count += 1

def trim_sched(games, day_games, night_games):
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


def load_data(data_file):
    """
    Load data from CSV file
    :param data_file: csv file
    :return:
    """
    # TODO allow for creation of Team objects from file
    with open(data_file, 'r') as f:
        reader = csv.reader(f)
        data = [item for item in reader]
    return data[0]


def load_teams(data_file):
    """
    Read csv and return a dict of Team objects. Key = level.  Value = list of teams
    :param data_file:
    :return: list of Teams
    """
    if not os.path.isfile(data_file):
        raise FileNotFoundError(f"File {data_file} does not exist")
    teams_dict = {}
    with open(data_file, 'r', newline='') as f:
        reader = csv.reader(f)
        for item in reader:
            if len(item) == 2:
                team = Team(item[0], item[1])
                if team.level not in teams_dict.keys():
                    teams_dict[team.level] = [team]
                else:
                    teams_dict[team.level].append(team)
            else:
                raise ValueError('CSV file was not formatted properly.  Requires exactly two fields: Name and Level')
        return teams_dict
    

def load_matchups(data_file):
    """
       Read csv and return a dict associating the number of matchups each team will have to face every other team
       at that league level.
       :param data_file:
       :return: list of Teams
       """
    if not os.path.isfile(data_file):
        raise FileNotFoundError(f"File {data_file} does not exist")
    matchups_dict = {}
    with open(data_file, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2 or not row[1].isdigit():
                raise ValueError("Invalid data format in CSV file")
            matchups_dict[row[0]] = int(row[1])
        return matchups_dict

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


def groups_three(teams: dict, matchups: dict):
    """
    Return a list of tuples containing team level, home team, and away team.
    teams dict will supply the home and away teams as well as league level.  Matches will only be made between teams
    at the same level.  matchups dict will determine the number of times each pair will be created for each level.
    At each level, there should be n * m * (n-1) games in total, where n = number of teams at the level and m = matchup
    :param teams:
    :param matchups:
    :return: list
    """
    master_list = [] # initialize the master list for all matches across all levels
    for key in teams.keys(): # Iterate over all levels
        i = 1 # Counter for matchups
        matches = matchups[key] # Set the number of matches per team pair
        for i in range(matches):
            games = it.combinations(teams[key],2) # Create match pairings for every Team in a level
            for game in games:
                if i % 2 == 0: # for odd iterations
                    master_list.append(game) # add to master list
                else:
                    r_game = (game[1], game[0]) # switch order to change home/away
                    master_list.append(r_game)
            i += 1
    return master_list

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


def create_schedule(games, teams, games_per_team, max_games_per_week):
    """
    Assign Home and Away Teams to a list of Games.

    Assignment must obey the following rules:
    * Teams must play exactly max_games_per_week Games
    * Teams must play every team before they can face a team an additional time.  This is based on gameday.
    * Teams must alternate between being Home and Away each time they face each other
    :param games: list of trimmed Games
    :param teams: List of Teams
    :param games_per_team: Number of Games each Team will be assigned
    :param max_games_per_week: Maximum number of Games each team can play per week_num
    :return: Modified list of Games
    """
    pass
    # i = 0 # game count
    # j = 0 # team count
    # for i in range(len(games)):
    #     assign_teams_to_game(teams[j], games[i])
    #     teams[j][0].home_game_count += 1
    #     teams[j][1].away_game_count += 1
    #     i += 1
    #     j += 1
    #     if j > len(teams) + 1:
    #         j = 0
    #     if i == games_per_team:
    #         break
