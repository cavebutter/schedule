# Tournament Scheduler

## Overview 
This application will generate a schedule based passed parameters:
* Number of Teams
* Number of Games to Be Played By Each Team
* Number of Fields Available
* Start and End Calendar Limits for the Tournament
* Days of the Week for Games to Be Played
* Maximum # of Games to be played by a team in a given week
* Time slots available per field

## Output
XLSX workbook with:
* One tab per team showing
  * Date
  * Time Slot
  * Field
  * Opponent
  * Home/Away
* One tab per field showing:
  * Date
  * Time Slot
  * Home Team
  * Away Team
* One New Workbook Per Tournament Day showing:
  * Field
  * Time Slot
  * Home Team
  * Away Team

## Development Approach
* Classes for Games and Teams
  * Games being combination of eligible game day, field, and time slot.  
  * Teams having just name, counters for home games, away games, and total

Create a list of all possible games, given tournament start, end, weekdays, and fields as Game objects

Add a field to Game class:  Week #.  Want to make sure that teams cannot play more than x games per week.  

Create home/away pairings equal to the number of games per team (passed as param).

Before assigning pairings to Games, perform the following checks:
* Teams play no more than x games per week
* Teams play every other team before re-playing an opponent

