import requests
from credentials import client_id

def get_mmr_ranges():
    queueId = 201 # LotV 1v1
    teamType = 0 # Arragend team
    leagueId = 5 # Master
    seasonId = 43
    access_token = ''
    payload = {'locale': 'en_US', 'access_token': access_token}
    url = f'https://eu.api.blizzard.com/data/sc2/league/{seasonId}/{queueId}/{teamType}/{leagueId}'
    r = requests.get(url, params=payload)
    print(r.json())
    # {'code': 404, 'type': 'BLZWEBAPI00000404', 'detail': 'Not Found'}

if __name__ == "__main__":
    get_mmr_ranges()