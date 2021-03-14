import os
import json


with open('season.json', 'r') as f:
    season = json.load(f)

new_schedule = []
for day in season:
    new_day = []
    for game in day:
        del game['team1WinLoss']
        del game['team2WinLoss']
        game['patternName'] = game['map']['patternName']
        del game['map']
        del game['team1Score']
        del game['team2Score']
        del game['generations']
        new_day.append(game) 
    new_schedule.append(new_day)

with open('newschedule.json', 'w') as f:
    json.dump(new_schedule, f, indent=4)
