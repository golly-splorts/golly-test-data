import json

for iseason in [0, 1]:

    # Confirm isPostseason is present and isPlayoffs is not
    # Confirm team1PostseasonWinLoss is present and team1PlayoffsWinLoss is not

    ###############
    # schedule
    with open('season%d/schedule.json'%(iseason), 'r') as f:
        schedule = json.load(f)

    for day in schedule:
        for game in day:
            if 'isPlayoffs' in game:
                if 'isPostseason' not in game:
                    game['isPostseason'] = game['isPlayoffs']
                del game['isPlayoffs']

    scheduleout = 'season%d/new_schedule.json'%(iseason)
    with open(scheduleout, 'w') as f:
        json.dump(schedule, f, indent=4)
    print(f"Wrote new schedule without isPlayoffs to {scheduleout}")


    ###############
    # season
    with open('season%d/season.json'%(iseason), 'r') as f:
        season = json.load(f)

    for day in season:
        for game in day:
            if 'isPlayoffs' in game:
                if 'isPostseason' not in game:
                    game['isPostseason'] = game['isPlayoffs']
                del game['isPlayoffs']

    seasonout = 'season%d/new_season.json'%(iseason)
    with open(seasonout, 'w') as f:
        json.dump(season, f, indent=4)
    print(f"Wrote new season without isPlayoffs to {seasonout}")


    ###############
    # bracket
    with open('season%d/bracket.json'%(iseason), 'r') as f:
        bracket = json.load(f)

    for series in bracket:
        miniseason = bracket[series]
        for day in miniseason:
            for game in day:
                if 'isPlayoffs' in game:
                    if 'isPostseason' not in game:
                        game['isPostseason'] = game['isPlayoffs']
                    del game['isPlayoffs']
                if 'team1PlayoffsWinLoss' in game:
                    if 'team1PostseasonWinLoss' not in game:
                        game['team1PostseasonWinLoss'] = game['team1PlayoffsWinLoss']
                    del game['team1PlayoffsWinLoss']
                if 'team2PlayoffsWinLoss' in game:
                    if 'team2PostseasonWinLoss' not in game:
                        game['team2PostseasonWinLoss'] = game['team2PlayoffsWinLoss']
                    del game['team2PlayoffsWinLoss']

    bracketout = 'season%d/new_bracket.json'%(iseason)
    with open(bracketout, 'w') as f:
        json.dump(bracket, f, indent=4)
    print(f"Wrote new bracket without isPlayoffs/teamXPlayoffsWins to {bracketout}")

    ###############
    # playoffs
    with open('season%d/postseason.json'%(iseason), 'r') as f:
        postseason = json.load(f)

    for series in postseason:
        miniseason = postseason[series]
        for day in miniseason:
            for game in day:
                if 'isPlayoffs' in game:
                    if 'isPostseason' not in game:
                        game['isPostseason'] = game['isPlayoffs']
                    del game['isPlayoffs']
                if 'team1PlayoffsWinLoss' in game:
                    if 'team1PostseasonWinLoss' not in game:
                        game['team1PostseasonWinLoss'] = game['team1PlayoffsWinLoss']
                    del game['team1PlayoffsWinLoss']
                if 'team2PlayoffsWinLoss' in game:
                    if 'team2PostseasonWinLoss' not in game:
                        game['team2PostseasonWinLoss'] = game['team2PlayoffsWinLoss']
                    del game['team2PlayoffsWinLoss']

    postout = 'season%d/new_post.json'%(iseason)
    with open(postout, 'w') as f:
        json.dump(postseason, f, indent=4)
    print(f"Wrote new postseason without isPlayoffs/teamXPlayoffsWins to {postout}")


