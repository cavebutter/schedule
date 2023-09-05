import sqlite3
from peewee import *

db = SqliteDatabase('pall.db')

class Level(Model):
    name = CharField()
    matchups = IntegerField()
    max_gpw = IntegerField()

    class Meta:
        database = db


class Field(Model):
    name = CharField()
    lights = BooleanField()

    class Meta:
        database = db


class Team(Model):
    name = CharField()
    level = ForeignKeyField(Level, backref='teams')

    class Meta:
        database = db


class LevelField(Model):
    level = ForeignKeyField(Level, backref='levelfields')
    field = ForeignKeyField(Field, backref='levelfields')

    class Meta:
        database = db


class GameType(Model):
    level = ForeignKeyField(Level, backref='gametypes')
    length = IntegerField()
    buffer = IntegerField()

    class Meta:
        database = db

class TimeSlot(Model):
    timeslot = CharField()
    start_time = CharField()
    end_time = CharField()
    game_type = ForeignKeyField(GameType, backref='timeslots')
    length = IntegerField()
    buffer = IntegerField()

    class Meta:
        database = db


class Game(Model):
    game = CharField()
    field = ForeignKeyField(Field, backref='games')
    start_time = CharField()
    end_time = CharField()
    hometeam = ForeignKeyField(Team, backref='games')
    awayteam = ForeignKeyField(Team, backref='games')
    level = ForeignKeyField(Level, backref='games')
    gametype = ForeignKeyField(GameType, backref='games')
    timeslot = ForeignKeyField(TimeSlot, backref='games')
    gamedate = DateField()

    class Meta:
        database = db



