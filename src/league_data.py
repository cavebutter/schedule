START_DATE = '2024-04-01'
END_DATE = '2024-06-30'

# These are the levels or leagues.  Data fields are: name, matchups, max_gpw
LEVELS = [('Tee Ball', 2, 1),
          ('Farm', 3, 2),
          ('AA', 3, 2),
          ('AAA', 3, 2),
          ('Minors', 3, 2),
          ('Majors', 4, 3)]

# These are the available playing fields in our universe.  Data fields are: name, lights
FIELDS = [('Hamilton-1', False),
          ('Hamilton-2', False),
          ('Hamilton-3', False),
          ('Victory-1', True),
          ('Victory-2', True),
          ('Victory-3', True),
          ('Victory-4', False),
          ('Victory-Grass', False)]


LEVELFIELD = [ # Level, Field
    ('Tee Ball', 'Hamilton-1'),
    ('Tee Ball', 'Hamilton-2'),
    ('Tee Ball', 'Hamilton-3'),
    ('Farm', 'Hamilton-1'),
    ('Farm', 'Hamilton-2'),
    ('Farm', 'Hamilton-3'),
    ('AA', 'Victory-1'),
    ('AA', 'Victory-2'),
    ('AA', 'Victory-3'),
    ('AAA', 'Victory-1'),
    ('AAA', 'Victory-2'),
    ('AAA', 'Victory-3'),
    ('Minors', 'Victory-1'),
    ('Minors', 'Victory-2'),
    ('Minors', 'Victory-3'),
    ('Majors', 'Victory-4'),
   ( 'Majors', 'Victory-3')
]

TEAMS_TBALL = [ # Name, Level
                ('Dodgers', 'Tee Ball'),
               ('Rays', 'Tee Ball'),
               ('Rangers', 'Tee Ball'),
               ('Mariners', 'Tee Ball'),
               ('Reds', 'Tee Ball'),
               ('Yankees', 'Tee Ball')]

TEAMS_FARM = [('Red Sox', 'Farm'), ('Blue Jays', 'Farm'),
              ('Marlins', 'Farm'), ('White Sox', 'Farm'),
              ('Tigers', 'Farm'),
              ('Royals', 'Farm'),
              ('Indians', 'Farm'),]

TEAMS_AA = [('Brewers', 'AA'),
            ('Brewers', 'AA'),
            ('Cardinals', 'AA'),
            ('Athletics', 'AA'),
            ('Angels', 'AA'),
            ('Orioles', 'AA'),
            ('Blue Jays', 'AA'),
            ]

TEAMS_AAA = [('Angels', 'AAA'),
             ('Orioles', 'AAA'),
             ('Blue Jays', 'AAA')]

TEAMS_MINORS = [('Tigers', 'Minors'),
                ('Royals',  'Minors'),
                ('Indians',  'Minors'),
                ('White Sox', 'Minors'),
                ('Cubs', 'Minors'),
                ('Red Sox', 'Minors'),
                ('Marlins' 'Minors'),]

TEAMS_MAJORS = [('Cubs', 'Majors'),
                ('Red Sox', 'Majors'),
                ('Marlins', 'Majors'),
                ('White Sox', 'Majors'),
                ('Tigers', 'Majors'),
                ('Royals', 'Majors'),
                ('Indians', 'Majors'),]

ALL_TEAMS = TEAMS_TBALL + TEAMS_FARM + TEAMS_AA + TEAMS_AAA + TEAMS_MINORS + TEAMS_MAJORS

GAMETYPES = [ # Level, length, time_before_game
    ('Tee Ball', 60, 30),
    ('Low Minors', 90, 30),
    ('High Minors', 120, 30),
    ('Practice', 120, 0)
]

TIMESLOTS = [ # name, start_time, end_time, game_type, length, buffer
    ('TB - Early Morning', '08:00', '09:00', 'Tee Ball', 60, 30),
    ('TB - Mid Morning', '09:30', '10:30', 'Tee Ball', 60, 30),
    ('TB - Late Morning', '11:00', '12:00', 'Tee Ball', 60, 30),
    ('Low Minors - Early Morning', '09:00', '10:30', 'Minors', 120, 30),
    ('Low Minors - Mid Morning', '11:00', '12:30', 'Minors', 120, 30),
    ('Low Minors - Early Afternoon', '13:00', '14:30', 'Minors', 120, 30),
    ('Low Minors - Late Afternoon', '15:00', '16:30', 'Minors', 120, 30),
    ('High Minors - Early Morning', '09:00', '11:00 ', 'High Minors', 120, 30),
    ('High Minors - Early Afternoon', '11:30', '13:30', 'High Minors', 120, 30),
    ('High Minors - Mid Afternoon', '14:00', '16:00', 'High Minors', 120, 30),
    ('High Minors - Late Afternoon', '16:30', '18:30', 'High Minors', 120, 30),
    ('High Minors - Weekday Evening', '17:30', '19:30', 'High Minors', 120, 30),
    ('Low Minors - Weekday Evening', '17:30', '19:00', 'Minors', 120, 30),
]