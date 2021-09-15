import copy
import os
import json
import glob


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))


broken_seasons = range(0, 14)

for season0 in broken_seasons:
    datadir = os.path.join(ROOT, f'season{season0}')

    teamfile = os.path.join(datadir, 'teams.json')
    seasfile = os.path.join(datadir, 'season.json')
    postfile = os.path.join(datadir, 'postseason.json')

    # # test
    # newseasfile = os.path.join(datadir, 'newseason.json')
    # newpostfile = os.path.join(datadir, 'newpostseason.json')
    # real
    newseasfile = os.path.join(datadir, 'season.json')
    newpostfile = os.path.join(datadir, 'postseason.json')
    
    # ---------------
    # team name-abbr map
    with open(teamfile, 'r') as f:
        teams = json.load(f)

    name2abbr = {}
    for t in teams:
        name2abbr[t['teamName']] = t['teamAbbr']
    
    # --------------
    # season
    with open(seasfile, 'r') as f:
        seas = json.load(f)

    newseas = []
    for day in seas:
        newday = []
        for game in day:
            newgame = copy.deepcopy(game)
            newgame['team1Abbr'] = name2abbr[newgame['team1Name']]
            newgame['team2Abbr'] = name2abbr[newgame['team2Name']]
            newday.append(newgame)
        newseas.append(newday)

    with open(newseasfile, 'w') as f:
        json.dump(newseas, f, indent=4)

    # --------------
    # postseason
    with open(postfile, 'r') as f:
        post = json.load(f)

    newpost = {}
    for series in post:
        dayslist = post[series]
        newdayslist = []
        for day in dayslist:
            newday = []
            for game in day:
                newgame = copy.deepcopy(game)
                newgame['team1Abbr'] = name2abbr[newgame['team1Name']]
                newgame['team2Abbr'] = name2abbr[newgame['team2Name']]
                newday.append(newgame)
            newdayslist.append(newday)
        newpost[series] = newdayslist

    with open(newpostfile, 'w') as f:
        json.dump(newpost, f, indent=4)

