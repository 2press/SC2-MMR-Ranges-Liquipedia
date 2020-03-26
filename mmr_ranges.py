import requests
import enum
from datetime import date

class League(enum.Enum):
    """StarCraft 2 Leagues."""
    Bronze = 0
    Silver = 1
    Gold = 2
    Platinum = 3
    Diamond = 4
    Master = 5

    def describe(self):
        """Return the name of the server."""
        if self.value == 0:
            desc = "Bronze"
        elif self.value == 1:
            desc = "Silver"
        elif self.value == 2:
            desc = "Gold"
        elif self.value == 3:
            desc = "Platinum"
        elif self.value == 4:
            desc = "Diamond"
        elif self.value == 5:
            desc = "Master"

        return desc

class Server(enum.Enum):
    """StarCraft 2 Server."""
    America = 1
    Europe = 2
    Korea = 3

    def id(self):
        """Return the id of the server used by the api."""
        return self.value

    def short(self):
        """Return the short name of the server."""
        if self.value == 1:
            desc = "us"
        elif self.value == 2:
            desc = "eu"
        elif self.value == 3:
            desc = "kr"

        return desc

class SC2API:
    """Wrapper for the SC2 api."""
    def __init__(self):
        """Init the sc2 api."""
        self.receive_new_access_token()

    def receive_new_access_token(self):
            """Receive a new acces token vai oauth."""
            from credentials import client_id, secret
            r = requests.get(
                'https://eu.battle.net/oauth/token',
                auth=(client_id, secret),
                params={'grant_type': 'client_credentials'})
            r.raise_for_status()
            self._access_token = r.json().get('access_token')

    def get_season(self, server: Server):
            """Collect the current season info."""
            api_url = ('https://eu.api.blizzard.com/sc2/'
                    f'ladder/season/{server.id()}')
            payload = {'locale': 'en_US', 'access_token': self._access_token}
            r = requests.get(api_url, params=payload)
            r.raise_for_status()
            return r.json()

    def get_mmr_ranges(self, league: League, seasonId: int , server: Server) -> dict:
        queueId = 201 # LotV 1v1
        teamType = 0 # Arragend team
        payload = {'locale': 'en_US', 'access_token': self._access_token}
        url = f'https://{server.short()}.api.blizzard.com/data/sc2/league/{seasonId}/{queueId}/{teamType}/{league.value}'
        r = requests.get(url, params=payload)
        r.raise_for_status()
        data = r.json()
        ranges = dict()
        for tier in data.get('tier'):
            id = int(tier.get('id')) + 1
            ranges[id] = (int(tier.get('min_rating')), int(tier.get('max_rating')))
        return ranges

if __name__ == "__main__":
    sc2api = SC2API()
    season_data = sc2api.get_season(Server.Europe)
    seasonId = season_data['seasonId']
    year = season_data['year']
    number = season_data['number']
    servers = [Server.Europe, Server.America, Server.Korea]
    with open('liquipedia_ranges.txt', 'w') as o:
        today = date.today().strftime('%B %d, %Y')
        season = f'{year} Season {number}'
        o.write('{| class="wikitable" style="text-align:center;"\n')
        o.write('|-\n')
        o.write('! rowspan=2 colspan=3 style="width:100px"| League\n')
        o.write('! colspan=4 style="width:560px" |MMR Floor\n')
        o.write('|-\n')
        o.write(f'|+ align="bottom" style="color: grey; font-weight:normal; font-size: 0.9em;" | League MMR Span, LotV 1v1 Ladder, {season}.<ref>{{{{cite web|url=https://develop.battle.net/documentation/api-reference/starcraft-2-game-data-api |title=StarCraft 2 Game Data API|accessdate={today}}}}}</ref>\n')
        o.write('|-\n')
        for server in servers:
            o.write(f'! style="width:140px" |{server.short().upper()}\n')
        o.write('|-\n')
        for league in [League.Master, League.Diamond, League.Platinum, League.Gold, League.Silver, League.Bronze]:
            o.write(f'!rowspan=4| [[File:{league.describe()}-medium.PNG|30px|]]\n')
            o.write(f'!rowspan=4| {league.describe()}\n')
            data = []
            for server in servers:
                data.append(sc2api.get_mmr_ranges(league, seasonId, server))
            for tier in range(1, 3):
                o.write('|-\n')
                o.write(f'|{tier} || ')
                if league == League.Master:
                    o.write(' || '.join([f'{string[tier][0]} - {string[tier][1]}' for string in data]))
                else:
                    o.write(' || '.join([f'{string[tier][0]}' for string in data]))
                o.write('\n')
        o.write('|}\n')