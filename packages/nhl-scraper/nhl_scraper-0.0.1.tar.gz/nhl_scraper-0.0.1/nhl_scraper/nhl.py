#!/usr/bin/python

import objectpath
import requests
import json
import datetime
import pandas as pd
from collections import defaultdict


class EndpointAdapter:
    NHL_URL = "https://statsapi.web.nhl.com/api/v1"

    def get(self, api):
        """Send an API request to the URI and return the response as JSON

        :param api: API to call
        :type uri: str
        :return: JSON document of the reponse
        :raises: RuntimeError if any response comes back with an error
        """
        response = requests.get("{}/{}".format(self.NHL_URL, api),
                                params={'format': 'json'})
        jresp = response.json()
        if "error" in jresp:
            raise RuntimeError(json.dumps(jresp))
        return jresp

    def teams_endpoint(self):
        return self.get("teams")

    def schedule_endpoint(self, date):
        return self.get("schedule?date={}".format(date.strftime("%Y-%m-%d")))

    def players_endpoint(self, team_ids):
        team_str = ",".join(str(n) for n in team_ids)
        return self.get("teams?teamId={}&expand=team.roster".format(team_str))


class Scraper:
    def __init__(self):
        self.ea = EndpointAdapter()
        self.teams_cache = None
        self.schedule_cache = {}
        self.players_cache = None

    def set_endpoint_adapter(self, ea):
        self.ea = ea

    def teams(self):
        """Get list of teams in the NHL

        :return: Team details
        :rtype: pandas.DataFrame

        >>> s.teams()
        id            name          city abbrev
        0    1          Devils    New Jersey    NJD
        1    2       Islanders      New York    NYI
        2    3         Rangers      New York    NYR
        3    4          Flyers  Philadelphia    PHI
        4    5        Penguins    Pittsburgh    PIT
        5    6          Bruins        Boston    BOS
        6    7          Sabres       Buffalo    BUF
        7    8       Canadiens      Montréal    MTL
        8    9        Senators        Ottawa    OTT
        9   10     Maple Leafs       Toronto    TOR
        10  12      Hurricanes      Carolina    CAR
        11  13        Panthers       Florida    FLA
        12  14       Lightning     Tampa Bay    TBL
        13  15        Capitals    Washington    WSH
        14  16      Blackhawks       Chicago    CHI
        15  17       Red Wings       Detroit    DET
        16  18       Predators     Nashville    NSH
        17  19           Blues     St. Louis    STL
        18  20          Flames       Calgary    CGY
        19  21       Avalanche      Colorado    COL
        20  22          Oilers      Edmonton    EDM
        21  23         Canucks     Vancouver    VAN
        22  24           Ducks       Anaheim    ANA
        23  25           Stars        Dallas    DAL
        24  26           Kings   Los Angeles    LAK
        25  28          Sharks      San Jose    SJS
        26  29    Blue Jackets      Columbus    CBJ
        27  30            Wild     Minnesota    MIN
        28  52            Jets      Winnipeg    WPG
        29  53         Coyotes       Arizona    ARI
        30  54  Golden Knights         Vegas    VGK
        """
        if self.teams_cache is None:
            r = self.ea.teams_endpoint()
            t = objectpath.Tree(r)
            colmap = {"id": "id", "teamName": "name", "locationName": "city",
                      "abbreviation": "abbrev"}
            path = "$..teams.({})".format(",".join(colmap.keys()))
            data = t.execute(path)
            df = pd.DataFrame(data=data, columns=colmap.keys())
            self.teams_cache = df.rename(columns=colmap)
        return self.teams_cache

    def games_count(self, start_date, end_date):
        """Returns a count of games for each team between a range of dates.

        The range of dates is inclusive.  The result is a dictionary, where the
        key is a team ID and the values is the number of games played within
        the date range.

        :param start_date: Starting date
        :type start_date: datetime.datetime
        :param end_date: Ending date (inclusive)
        :type end_date: datetime.datetime
        :return: dict of keys (teamID) to values (number of games played)
        :rtype: defaultdict

        >>> s.games_count(datetime.datetime(2019,10,1),datetime.datetime(2019,10,6))
		>>> defaultdict(<function hockey_scraper.nhl.Scraper.games_count.<locals>.<lambda>()>,
            {9: 2, 10: 3, 15: 3, 19: 2, 23: 2, 22: 2, 28: 3, 54: 2, 13: 2,
             14: 3, 52: 3, 3: 2, 7: 2, 5: 2, 8: 2, 12: 3, 30: 2, 18: 2,
             6: 2, 25: 3, 20: 2, 21: 2, 53: 2, 24: 2, 16: 1, 4: 1, 1: 2,
             2: 2, 29: 2, 17: 2, 26: 1})
        """ # noqa
        if start_date > end_date:
            raise RuntimeError("End date must be beyond start")
        cur_date = start_date
        tot_gc = defaultdict(lambda: 0)
        while cur_date <= end_date:
            teams_playing = self._teams_playing_one_day(cur_date)
            for team in teams_playing:
                tot_gc[team] += 1
            cur_date = cur_date + datetime.timedelta(days=1)
        return tot_gc

    def players(self):
        """Returns the full list of all players in the NHL.

        Each player is returned with their teamID and playerID.

        :return: All players
        :rtype: pandas.DataFrame
        """
        if self.players_cache is None:
            team_df = self.teams()
            self.players_cache = self.ea.players_endpoint(
                team_df["id"].tolist())

        columns = ["teamId", "playerId", "name"]
        all_players = []
        for team in self.players_cache["teams"]:
            team_id = team["id"]
            for plyr in team["roster"]["roster"]:
                player_id = plyr["person"]["id"]
                player_name = plyr["person"]["fullName"]
                all_players.append({columns[0]: team_id,
                                    columns[1]: player_id,
                                    columns[2]: player_name})
        return pd.DataFrame(data=all_players, columns=columns)

    def _teams_playing_one_day(self, date):
        if date not in self.schedule_cache:
            r = self.ea.schedule_endpoint(date)
            t = objectpath.Tree(r)
            data = t.execute("$..dates[0]..games.teams..(id)")
            self.schedule_cache[date] = []
            for team in data:
                self.schedule_cache[date].append(team["id"])
        return self.schedule_cache[date]
