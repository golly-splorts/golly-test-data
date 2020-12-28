import os
import json


NSEASONS = 3
for iseason in range(NSEASONS):
    seasondir = "season%d"%(iseason)


    #####################
    # load team data

    teamsfile = os.path.join(seasondir, 'teams.json')

    with open(teamsfile, 'r') as f:
        teams = json.load(f)

    # -----------
    # team function defs

    def get_team_color(teamName):
        for team in teams:
            if team['teamName'] == teamName:
                return team['teamColor']

    def get_team_league(teamName):
        for team in teams:
            if team['teamName'] == teamName:
                return team['league']


    #####################
    # check games

    # -----------
    # game function defs

    def check_id(game):
        if 'id' not in game:
            raise Exception(f"Error: missing game id from game {game}")
    def check_name_color_match(game):
        """For a given game ensure the team name matches the team color"""
        t1 = game['team1Name']
        t1c = game['team1Color']
        if t1c != get_team_color(t1):
            raise Exception(f"Error in game {game['id']} of day {game['day']}: team1 color was {t1c}, should have been {get_team_color(t1)}")
        t2 = game['team1Name']
        t2c = game['team1Color']
        if t2c != get_team_color(t2):
            raise Exception(f"Error in game {game['id']} of day {game['day']}: team2 color was {t2c}, should have been {get_team_color(t2)}")

    def check_score(game):
        t1s = game['team1Score']
        t2s = game['team2Score']
        if t1s==t2s:
            raise Exception(f"Error in game {game['id']} of day {game['day']}: game is tied! {team1Score}-{team2Score}")
        if t1s < 0 or t2s < 0:
            raise Exception(f"Error in game {game['id']} of day {game['day']}: negative score ({t1s})-({t2s})")

    def check_league(game):
        league = game['league']
        t1 = game['team1Name']
        t2 = game['team2Name']
        t1lea = get_team_league(t1)
        t2lea = get_team_league(t2)
        if (t1lea!=league) or (t2lea!=league):
            raise Exception(f"Error in game {game['id']} of day {game['day']}: league information does not match: {t1}:{t1lea}, {t2}:{t2lea}")

    def check_id(game):
        if 'id' not in game.keys():
            print(game)
            raise Exception(f"Error in game on day {game['day']}: no id found")

    def check_pattern(game):
        if 'patternName' not in game.keys():
            raise Exception(f"Error in game {game['id']} of day {game['day']}: game is missing a map!")

    def check_map(game):
        if 'map' not in game.keys():
            raise Exception(f"Error in game {game['id']} of day {game['day']}: game is missing a map!")
        mapp = game['map']
        # required keys that must be present
        req_keys = [
            'mapName',
            'mapZone1Name',
            'mapZone2Name',
            'mapZone3Name',
            'mapZone4Name',
            'initialConditions1',
            'initialConditions2',
            'rows',
            'columns',
            'cellSize',
            'patternName'
        ]
        # unused keys that should not be present
        unreq_keys = [
            'url',
            'patternId'
        ]

        for rk in req_keys:
            if rk not in mapp:
                raise Exception("Error in game {game['id']} of day {game['day']}: game map is missing key \"{rk}\"!")
        #for urk in unreq_keys:
        #    if urk in mapp:
        #        raise Exception("Error in game {game['id']} of day {game['day']}: game map should not have key \"{urk}\"!")

    def check_wl(game):
        req_keys = ['team1WinLoss', 'team2WinLoss']
        for rk in req_keys:
            if rk not in game:
                raise Exception("Error in game {game['id']} of day {game['day']}: game map is missing key \"{rk}\"!")

        wlsum1 = game['team1WinLoss'][0] + game['team1WinLoss'][1]
        wlsum2 = game['team1WinLoss'][0] + game['team1WinLoss'][1]
        if (wlsum1!=(game['day'])):
            print(game)
            raise Exception(f"Error in game {game['id']} of season {game['season']} day {game['day']}: win loss record for team 1 sums to {wlsum1}, should sum to {game['day']}")
        if (wlsum2!=(game['day'])):
            raise Exception(f"Error in game {game['id']} of season {game['season']} day {game['day']}: win loss record for team 2 sums to {wlsum2}, should sum to {game['day']}")

    def check_game_season(game, correct_season):
        if (iseason != game['season']):
            raise Exception(f"Error in game {game['id']} of season {game['season']} day {game['day']}: season should be {correct_season}")

    def check_season_day(day):
        if len(day) != len(teams)//2:
            raise Exception(f"Error: day {day[0]['day']} has length {len(day)} but should have length {len(teams)//2}")

    def check_bracket_day(day, series):
        series_gpd = {
            'LDS': 4,
            'LCS': 2,
            'WS': 1
        }
        if series not in series_gpd:
            raise Exception(f"Error: series name {series} not in {', '.join(series_gpd.keys())}")
        if len(day) != series_gpd[series]:
            raise Exception(f"Error: bracket for series {series} has incorrect number of games ({len(day)}, should be {series_gpd[series]})")

    # -----------
    # schedule

    schedfile = os.path.join(seasondir, 'schedule.json')

    print("***************************")
    print(f"Now checking {schedfile}")

    with open(schedfile, 'r') as f:
        sched = json.load(f)

    sched_team_names = set()
    for iday, day in enumerate(sched):
        check_season_day(day)
        games = day
        for igame, game in enumerate(games):
            t1 = game['team1Name']
            t2 = game['team1Name']

            check_id(game)
            check_name_color_match(game)
            check_league(game)
            check_pattern(game)
            check_game_season(game, iseason)

            sched_team_names.add(t1)
            sched_team_names.add(t2)

    if len(sched_team_names) != len(teams):
        raise Exception(f"Error: number of teams found in schedule was {len(sched_team_names)}, number of teams is {len(teams)}")

    for team in teams:
        if team['teamName'] not in sched_team_names:
            raise Exception(f"Error: team name {team['teamName']} not found in schedule.json")


    # -----------
    # season

    seasonfile = os.path.join(seasondir, 'season.json')

    print("***************************")
    print(f"Now checking {seasonfile}")

    with open(seasonfile, 'r') as f:
        season = json.load(f)

    season_team_names = set()
    for iday, day in enumerate(season):
        check_season_day(day)
        games = day
        for igame, game in enumerate(games):
            t1 = game['team1Name']
            t2 = game['team2Name']

            check_id(game)
            check_name_color_match(game)
            check_score(game)
            check_league(game)
            check_id(game)
            check_map(game)
            check_wl(game)
            check_game_season(game, iseason)

            season_team_names.add(t1)
            season_team_names.add(t2)

    if len(season_team_names) != len(teams):
        raise Exception(f"Error: number of teams found in season was {len(season_team_names)}, number of teams is {len(teams)}")

    for team in teams:
        if team['teamName'] not in season_team_names:
            raise Exception(f"Error: team name {team['teamName']} not found in season.json")


    # -----------
    # bracket
    bracketfile = os.path.join(seasondir, 'bracket.json')

    print("***************************")
    print(f"Now checking {bracketfile}")

    with open(bracketfile, 'r') as f:
        bracket = json.load(f)

    for series in bracket:
        miniseason = bracket[series]
        for iday, day in enumerate(miniseason):
            check_bracket_day(day, series)

    # Verify series are the correct lengths
    ldslen = len(bracket['LDS'])
    if ldslen!=5:
        raise Exception(f"Error: bracket LDS length is invalid: {ldslen} games, should be 5")

    lcslen = len(bracket['LCS'])
    if lcslen!=5:
        raise Exception(f"Error: postseason LCS length is invalid: {lcslen} games, should be 5")

    wslen = len(bracket['WS'])
    if wslen!=7:
        raise Exception(f"Error: postseason WS length is invalid: {wslen} games, should be 7")

    # -----------
    # postseason

    postseasonfile = os.path.join(seasondir, 'postseason.json')

    print("***************************")
    print(f"Now checking {postseasonfile}")

    postseason_team_names = set()
    with open(postseasonfile, 'r') as f:
        postseason = json.load(f)

    for series in postseason:
        miniseason = postseason[series]
        for iday, day in enumerate(miniseason):
            games = day
            for igame, game in enumerate(games):
                t1 = game['team1Name']
                t2 = game['team2Name']

                check_id(game)
                check_name_color_match(game)
                check_score(game)
                if series != 'WS':
                    check_league(game)
                check_map(game)
                check_game_season(game, iseason)

                postseason_team_names.add(t1)
                postseason_team_names.add(t2)

    team_names = set()
    for team in teams:
        team_names.add(team['teamName'])
    for postseason_team_name in postseason_team_names:
        if postseason_team_name not in team_names:
            raise Exception(f"Error: invalid team name {postseason_team_name} found in postseason.json")

    # Verify series are the correct lengths
    ldslen = len(postseason['LDS'])
    if ldslen>5 or ldslen<3:
        raise Exception(f"Error: postseason LDS length is invalid: {ldslen} games")

    lcslen = len(postseason['LCS'])
    if lcslen>5 or lcslen<3:
        raise Exception(f"Error: postseason LCS length is invalid: {lcslen} games")

    wslen = len(postseason['WS'])
    if wslen>7 or wslen<4:
        raise Exception(f"Error: postseason WS length is invalid: {wslen} games")


print("***************************")
print("Everything is okay")
