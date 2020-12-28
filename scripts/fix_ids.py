import uuid
import json

for iseason in [2]:

    # replace ids in season.json
    with open('season%d/season.json'%(iseason), 'r') as f:
        season = json.load(f)
    
    for day in season:
        for game in day:
            game['id'] = str(uuid.uuid4())
    
    seasonout = 'season%d/new_season.json'%(iseason)
    with open(seasonout, 'w') as f:
        json.dump(season, f, indent=4)
    print(f"Wrote new season with new game ids to {seasonout}")
    
    # replace ids in postseason.json
    with open('season%d/postseason.json'%(iseason), 'r') as f:
        postseason = json.load(f)
    
    for series in postseason:
        miniseason = postseason[series]
        for day in miniseason:
            for game in day:
                game['id'] = str(uuid.uuid4())
        postseason[series] = miniseason
    
    postout = 'season%d/new_postseason.json'%(iseason)
    with open(postout, 'w') as f:
        json.dump(postseason, f, indent=4)
    print(f"Wrote new season with new game ids to {postout}")
