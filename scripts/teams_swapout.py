import os
import json


season = 2
write = True


seasondir = f'season{season}'

def _make_path(filename):
    return os.path.join(seasondir, filename)

oldteamsfile = _make_path('old_teams.json')
newteamsfile = _make_path('new_teams.json')
teamsfile    = _make_path('teams.json')
schedulefile = _make_path('schedule.json')
bracketfile  = _make_path('bracket.json')
seasonfile   = _make_path('season.json')
postfile     = _make_path('postseason.json')

with open(oldteamsfile, 'r') as f:
    oldteams = json.load(f)
    
with open(newteamsfile, 'r') as f:
    newteams = json.load(f)

if len(oldteams) != len(newteams):
    raise Exception(f"Error: mismatch in number of teams in {oldteamsfile} and {newteamsfile}")

# fix this stupid duplicate color mistake
dcs = 'Delaware Corporate Shells'
dcscolor = '#a0e7e8'

team_name_map = {}
for oldteam in oldteams:
    old_name = oldteam['teamName']
    if old_name == dcs:
        oldteam['teamColor'] = dcscolor
    for team in newteams:
        if oldteam['teamColor'] == team['teamColor']:
            team_name = team['teamName']
            team_name_map[old_name] = team_name
            break

if len(team_name_map) != len(oldteams):
    print([j['teamName'] for j in oldteams])
    print(list(team_name_map.keys()))
    raise Exception(f"Error: size mismatch in number of teams {len(oldteams)} and size of old-new mapping {len(team_name_map)}")




for team in oldteams:
    if team['teamName']==dcs:
        team['teamColor'] = dcscolor
    team['teamName'] = team_name_map[team['teamName']]

teams = oldteams

with open(teamsfile, 'w') as f:
    json.dump(teams, f, indent=4)



with open(schedulefile, 'r') as f:
    schedule = json.load(f)

for day in schedule:
    for game in day:
        if game['team1Name']==dcs:
            game['team1Color'] = dcscolor
        if game['team2Name']==dcs:
            game['team2Color'] = dcscolor
        game['team1Name'] = team_name_map[game['team1Name']]
        game['team2Name'] = team_name_map[game['team2Name']]

if write:
    with open(schedulefile, 'w') as f:
        json.dump(schedule, f, indent=4)



with open(seasonfile, 'r') as f:
    season = json.load(f)

for day in season:
    for game in day:
        if game['team1Name']==dcs:
            game['team1Color'] = dcscolor
        if game['team2Name']==dcs:
            game['team2Color'] = dcscolor
        game['team1Name'] = team_name_map[game['team1Name']]
        game['team2Name'] = team_name_map[game['team2Name']]

if write:
    with open(seasonfile, 'w') as f:
        json.dump(season, f, indent=4)



with open(bracketfile, 'r') as f:
    bracket = json.load(f)

for series in bracket:
    miniseason = bracket[series]
    for day in miniseason:
        for game in day:
            try:
                if game['team1Name']==dcs:
                    game['team1Color'] = dcscolor
                if game['team2Name']==dcs:
                    game['team2Color'] = dcscolor
                game['team1Name'] = team_name_map[game['team1Name']]
                game['team2Name'] = team_name_map[game['team2Name']]
            except KeyError:
                pass

if write:
    with open(bracketfile, 'w') as f:
        json.dump(bracket, f, indent=4)


with open(postfile, 'r') as f:
    postseason = json.load(f)

for series in postseason:
    miniseason = postseason[series]
    for day in miniseason:
        for game in day:
            try:
                if game['team1Name']==dcs:
                    game['team1Color'] = dcscolor
                if game['team2Name']==dcs:
                    game['team2Color'] = dcscolor
                game['team1Name'] = team_name_map[game['team1Name']]
                game['team2Name'] = team_name_map[game['team2Name']]
            except KeyError:
                pass

if write:
    with open(postfile, 'w') as f:
        json.dump(postseason, f, indent=4)
