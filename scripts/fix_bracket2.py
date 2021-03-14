import copy
import os
import json


with open('postseason.json', 'r') as f:
    post = json.load(f)

newpost = {}
for series in post:
    miniseason = post[series]
    newminiseason = []
    for day in miniseason:
        newday = []
        for game in day:
            newgame = copy.deepcopy(game)
            del newgame['team1PostseasonWinLoss']
            del newgame['team2PostseasonWinLoss']
            del newgame['team1SeriesWinLoss']
            del newgame['team2SeriesWinLoss']
            newgame['patternName'] = game['map']['patternName']
            del newgame['map']
            del newgame['day']
            del newgame['team1Color']
            del newgame['team2Color']
            del newgame['team1Score']
            del newgame['team2Score']
            del newgame['generations']
            newday.append(newgame)
        newminiseason.append(newday)
    newpost[series] = newminiseason
    
with open('newbracket.json', 'w') as f:
    json.dump(newpost, f, indent=4)
