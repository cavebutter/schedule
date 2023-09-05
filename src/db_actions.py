from src.model import *
from src.league_data import *
import src.teams as t
import os

if __name__ == '__main__':
    if not os.path.isfile(r'C:\Users\JayCohen\OneDrive - The Canton Group\dev\schedule\src\pall.db'):
        db = SqliteDatabase('pall.db')

        # Create the database tables
        db.create_tables([Level, Field, Team, LevelField, GameType, TimeSlot, Game])

        # Insert data into the database
        Level.insert_many(LEVELS).execute()

        Field.insert_many(FIELDS).execute()

        LevelField.insert_many(LEVELFIELD).execute()

        Team.insert_many(ALL_TEAMS).execute()

        GameType.insert_many(GAMETYPES).execute()

        TimeSlot.insert_many(TIMESLOTS).execute()

    else:
        db.connect('pall.db')

    # Get matchups for given level
    level = 'Farm'
    query = Team.select().where(Team.level == level)
    level_obj =  Level.get(Level.name == level)
    matchups = level_obj.matchups
    teams = t.add_bye(query, level)

    for team in teams:
        print(team)

    db.close()