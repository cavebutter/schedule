import os
import itertools as it
import csv
import os.path

night_games_only = [0,1,2,3,4]
day_games_only = [5,6]


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
        reader = csv.reader(f, skipinitialspace=True)
        next(reader, None)
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
        reader = csv.reader(f, skipinitialspace=True)
        next(reader, None)
        for row in reader:
            if len(row) != 2 or not row[1].isdigit():
                raise ValueError("Invalid data format in CSV file")
            matchups_dict[row[0]] = int(row[1])
        return matchups_dict


def add_bye(teams:dict)->dict:
    """
    For each level in the teams dict, if the number of teams is odd, add a Bye team.  Return the modified dict.
    :param teams:
    :return:
    """
    for key in teams:
        if len(teams[key]) % 2 == 1:
            teams[key].append(Team('Bye', key))
    return teams

def groups_two(teams):
    """
    Return all possible combinations of team pairs
    :type teams: str
    :param teams:
    :return:
    """
    groups = list(it.combinations(teams,2))
    return groups


def create_matchups(teams: dict, matchups: dict):
    """
    Return a list of tuples containing team level, home team, and away team.
    teams dict will supply the home and away teams as well as league level.  Matches will only be made between teams
    at the same level.  matchups dict will determine the number of times each pair will be created for each level.
    At each level, there should be (n * m * (n-1)) / 2 games in total, where n = number of teams at the level and m = matchup
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
