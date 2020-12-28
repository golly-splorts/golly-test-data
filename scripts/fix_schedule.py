import uuid
import json

# fix schedule - trimmed version of season
# remove playoffs wins

for iseason in [0, 1]:

    # Regular season schedule
    with open('season%d/season.json'%(iseason), 'r') as f:
        season = json.load(f)
    
    new_schedule = []
    for day in season:
        new_day = []
        for game in day:
            new_game = {}
            new_game['team1Name']   = game['team1Name']
            new_game['team2Name']   = game['team2Name']
            new_game['team1Color']  = game['team1Color']
            new_game['team2Color']  = game['team2Color']
            new_game['id']          = game['id']
            new_game['season']      = game['season']
            new_game['day']         = game['day']
            new_game['isPostseason']  = game['isPostseason']
            new_game['league']      = game['league']
            new_game['patternName'] = game['map']['patternName']
            new_day.append(new_game)
        new_schedule.append(new_day)
    
    schedout = 'season%d/new_schedule.json'%(iseason)
    with open(schedout, 'w') as f:
        json.dump(new_schedule, f, indent=4)
    print(f"Wrote new schedule matching season to {schedout}")

    # Postseason bracket
    with open('season%d/postseason.json'%(iseason), 'r') as f:
        postseason = json.load(f)

    with open('season%d/bracket.json'%(iseason), 'r') as f:
        oldbracket = json.load(f)

    series_lengths = {
        'LDS': 5,
        'LCS': 5,
        'WS': 7,
    }

    new_bracket = {}
    for series in postseason:
        miniseason = postseason[series]
        minibracket = oldbracket[series]

        new_bracket[series] = []
        for season_day, bracket_day in zip(miniseason, minibracket):
            new_day = []
            for season_game, bracket_game in zip(season_day, bracket_day):
                bracket_game['id'] = season_game['id']
                new_day.append(bracket_game)
            new_bracket[series].append(new_day)

        for i in range(len(minibracket) - len(miniseason)):
            new_day = []
            for bracket_game in bracket_day:
                bracket_game['id'] = str(uuid.uuid4())
                new_day.append(bracket_game)
            new_bracket[series].append(new_day)

    brackout = 'season%d/new_bracket.json'%(iseason)
    with open(brackout, 'w') as f:
        json.dump(new_bracket, f, indent=4)
    print(f"Wrote new bracket matching postseason to {brackout}")

