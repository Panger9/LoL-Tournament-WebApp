class User:

    def __init__(self, id=0, puuid='', token=''):
        self._id = id
        self._puuid = puuid
        self._token = token

    def get_id(self):
        return self._id
    
    def set_id(self, id):
        self._id = id

    def get_puuid(self):
        return self._puuid
    
    def set_puuid(self, puuid):
        self._puuid = puuid

    def get_token(self):
        return self._token
    
    def set_token(self, token):
        self._token = token

    def __str__(self):
        return f"User: {self._id}, {self._puuid}, {self._token}"

    @staticmethod
    def umwandlung(dic: dict):
        obj = User()
        obj.set_id(dic['id'])
        obj.set_puuid(dic['puuid'])
        obj.set_token(dic['token'])
        return obj