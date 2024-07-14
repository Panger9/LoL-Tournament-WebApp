import requests

class RiotAPIIntegration:
    def __init__(self):
        self.api_key = 'RGAPI-b5e5d794-4e3f-402a-9e31-bef5fc395742'

    def fetch_puuid(self, sumName, tagLine):
        url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{sumName}/{tagLine}?api_key={self.api_key}'
        response = requests.get(url)
        return self._handle_response(response)

    def fetch_id(self, puuid):
        url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.api_key}'
        response = requests.get(url)
        return self._handle_response(response)

    def fetch_playerinfo(self, sum_id):
        url = f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{sum_id}?api_key={self.api_key}'
        response = requests.get(url)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Failed to fetch data from Riot API'}, response.status_code
