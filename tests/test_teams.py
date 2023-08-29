from src.general import load_data
from src.teams import *
from src.games import Game
from collections import Counter
import pytest


def test_load_data():
    # Arrange
    data_file = "data/time_slots.csv"

    # Act
    data_list = load_data(data_file)

    # Assert
    assert isinstance(data_list, list)


class TestTeam:

    #  Tests that a Team object can be created with valid inputs
    def test_create_team_with_valid_inputs(self):
        # Arrange
        team_name = "Team A"
        level = "Beginner"

        # Act
        team = Team(team_name, level)

        # Assert
        assert team.team_name == team_name
        assert team.level == level
        assert team.home_game_count == 0
        assert team.away_game_count == 0

    #  Tests that the home_game_count is incremented by 1
    def test_increment_home_count(self):
        # Arrange
        team_name = "Team A"
        level = "Beginner"
        team = Team(team_name, level)

        # Act
        team.increment_home_count()

        # Assert
        assert team.home_game_count == 1

    #  Tests that the away_game_count is incremented by 1
    def test_increment_away_count(self):
        # Arrange
        team_name = "Team A"
        level = "Beginner"
        team = Team(team_name, level)

        # Act
        team.increment_away_count()

        # Assert
        assert team.away_game_count == 1

    #  Tests that a Team object cannot be created with an empty team_name
    def test_create_team_with_empty_team_name(self):
        # Arrange
        team_name = ""
        level = "Beginner"

        # Act and Assert
        with pytest.raises(ValueError):
            Team(team_name, level)

    #  Tests that a Team object cannot be created with an empty level
    def test_create_team_with_empty_level(self):
        # Arrange
        team_name = "Team A"
        level = ""

        # Act and Assert
        with pytest.raises(ValueError):
            Team(team_name, level)


class TestAssignTeamsToGame:

    #  Tests that the method assigns the first team in the match tuple to the home team and the second team to the away team, and increments the home_game_count and away_game_count for the respective teams.
    def test_assign_teams_to_game_happy_path(self):
        # Arrange
        team1 = Team("Team 1", "Level 1")
        team2 = Team("Team 2", "Level 2")
        game = Game("Field 1", "10:00 AM", "2022-01-01")

        # Act
        game.assign_teams_to_game((team1, team2))

        # Assert
        assert game.hometeam == team1
        assert game.awayteam == team2
        assert team1.home_game_count == 1
        assert team2.away_game_count == 1

    #  Tests that the method can handle assigning multiple games to the same team, and increments the home_game_count and away_game_count for the team accordingly.
    def test_assign_teams_to_game_multiple_games(self):
        # Arrange
        team = Team("Team 1", "Level 1")
        game1 = Game("Field 1", "10:00 AM", "2022-01-01")
        game2 = Game("Field 2", "2:00 PM", "2022-01-02")

        # Act
        game1.assign_teams_to_game((team, Team("Team 2", "Level 2")))
        game2.assign_teams_to_game((team, Team("Team 3", "Level 3")))

        # Assert
        assert game1.hometeam == team
        assert game2.hometeam == team
        assert team.home_game_count == 2

    #  Tests that the method can handle assigning multiple games to different teams, and increments the home_game_count and away_game_count for the respective teams.
    def test_assign_teams_to_game_different_teams(self):
        # Arrange
        team1 = Team("Team 1", "Level 1")
        team2 = Team("Team 2", "Level 2")
        game1 = Game("Field 1", "10:00 AM", "2022-01-01")
        game2 = Game("Field 2", "2:00 PM", "2022-01-02")

        # Act
        game1.assign_teams_to_game((team1, team2))
        game2.assign_teams_to_game((team2, team1))

        # Assert
        assert game1.hometeam == team1
        assert game1.awayteam == team2
        assert game2.hometeam == team2
        assert game2.awayteam == team1
        assert team1.home_game_count == 1
        assert team1.away_game_count == 1
        assert team2.home_game_count == 1
        assert team2.away_game_count == 1

    #  Tests the edge cases where the first element of 'match' is not an instance of the 'Team' class and raises a ValueError, and where the second element of 'match' is not an instance of the 'Team' class and raises a ValueError.
    # def test_assign_teams_to_game_edge_cases(self):
    #     # Arrange
    #     team = Team("Team 1", "Level 1")
    #     game = Game("Field 1", "10:00 AM", "2022-01-01")
    #
    #     # Assert ValueError is raised when first element of 'match' is not an instance of the 'Team' class
    #     with pytest.raises(ValueError):
    #         game.assign_teams_to_game(("Not a Team", team))
    #
    #     # Assert ValueError is raised when second element of 'match' is not an instance of the 'Team' class
    #     with pytest.raises(ValueError):
    #         game.assign_teams_to_game((team, "Not a Team"))


class TestLoadTeams:

    #  Tests that the function can load a csv file containing multiple teams with different levels
    def test_csv_file_with_multiple_teams_with_different_levels(self, mocker):
        # Arrange
        data_file = 'multiple_teams_different_levels.csv'
        mocker.patch('os.path.isfile', return_value=True)
        mocker.patch('builtins.open', mocker.mock_open(read_data='team1,level1\nteam2,level2\nteam3,level3\n'))

        # Act
        result = load_teams(data_file)

        # Assert
        assert len(result['level1']) == 1
        assert len(result['level2']) == 1
        assert len(result['level3']) == 1

    #  Tests that the function can load a csv file containing multiple teams with the same level
    def test_csv_file_with_multiple_teams_with_same_level(self, mocker):
        # Arrange
        data_file = 'multiple_teams_same_level.csv'
        mocker.patch('os.path.isfile', return_value=True)
        mocker.patch('builtins.open', mocker.mock_open(read_data='team1,level1\nteam2,level1\nteam3,level1\n'))

        # Act
        result = load_teams(data_file)

        # Assert
        assert len(result['level1']) == 3

class TestLoadMatchups:

    #  Tests that the function can successfully load a valid CSV file and return a dictionary with the correct key-value pairs.
    #  Note:  I am dumb.  You will have to replace the path to datafile with the absolute path on your implementation
    def test_valid_csv_file(self, mocker):
        # Arrange
        data_file = 'C:\\Users\\JayCohen\\OneDrive - The Canton Group\\dev\\schedule\\data\\matchups.csv'
        expected_result = {'tball': 1, 'farm': 2, 'aa': 3}

        # Act
        result = load_matchups(data_file)

        # Assert
        assert result == expected_result

class TestGroupsThree:

    # Test that the number of matches produced = (n * m * (n-1)) / 2.
    def test_groups_three_count(self):
        # Arrange
        teams_file = 'C:\\Users\\JayCohen\\OneDrive - The Canton Group\\dev\\schedule\\data\\small_even_teams.csv'
        matchups_file = 'C:\\Users\\JayCohen\\OneDrive - The Canton Group\\dev\\schedule\\data\\matchups.csv'
        expected_result = 12

        # Act
        teams = load_teams(teams_file)
        matches = load_matchups(matchups_file)
        result = create_matchups(teams, matches)

        # Assert
        assert len(result) == expected_result


    # Test that the matches created are the correct matches for two levels
    def test_groups_three(self):
        # Arrange
        teams = {
            'level1': ['team1', 'team2', 'team3', 'team4'],
            'level2': ['team5', 'team6']
        }
        matchups = {
            'level1': 1,
            'level2': 2
        }
        expected_result = [('team1', 'team2'), ('team1', 'team3'), ('team1', 'team4'), ('team2', 'team3'),
                            ('team2', 'team4'), ('team3', 'team4'), ('team5', 'team6'), ('team6', 'team5')]


        # Act
        result = create_matchups(teams, matchups)

        # Convert tuples to strings
        expected_result = [str(matchup) for matchup in expected_result]
        result = [str(matchup) for matchup in result]

        # Assert
        assert Counter(result) == Counter(expected_result)


class TestAddBye:

    #  Tests that the function correctly adds a Bye team for each level with an even number of teams
    def test_even_teams(self):
        # Arrange
        teams = {
            'level1': [Team('Team1', 'level1'), Team('Team2', 'level1')],
            'level2': [Team('Team3', 'level2'), Team('Team4', 'level2')]
        }

        # Act
        result = add_bye(teams)

        # Assert
        assert len(result['level1']) == 2
        assert len(result['level2']) == 2
        assert result['level1'][0].team_name == 'Team1'
        assert result['level1'][1].team_name == 'Team2'
        assert result['level2'][0].team_name == 'Team3'
        assert result['level2'][1].team_name == 'Team4'

    #  Tests that the function correctly adds a Bye team for each level with an odd number of teams
    def test_odd_teams(self):
        # Arrange
        teams = {
            'level1': [Team('Team1', 'level1'), Team('Team2', 'level1'), Team('Team3', 'level1')],
            'level2': [Team('Team4', 'level2'), Team('Team5', 'level2')]
        }

        # Act
        result = add_bye(teams)

        # Assert
        assert len(result['level1']) == 4
        assert len(result['level2']) == 2