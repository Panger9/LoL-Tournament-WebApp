import requests

class RiotAPIIntegration:
    def __init__(self):
        self.api_key = 'RGAPI-77ca8c7a-1eb2-469e-82d6-23cba9ef519d'

    def fetch_puuid(self, sumName, tagLine):
        url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{sumName}/{tagLine}?api_key={self.api_key}'
        response = requests.get(url)
        return self._handle_response(response)

    def fetch_sum_id(self, puuid):
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
