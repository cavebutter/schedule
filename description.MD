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