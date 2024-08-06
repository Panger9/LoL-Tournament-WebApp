class User:
    def __init__(self, id=0, puuid='', token='', gameName='', tagLine='', profileIconId=0, summonerLevel=0, tier="UNRANKED", rank=''):
        self._id = id
        self._puuid = puuid
        self._token = token
        self._gameName = gameName
        self._tagLine = tagLine
        self._profileIconId = profileIconId
        self._summonerLevel = summonerLevel
        self._tier = tier
        self._rank = rank

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

    def get_gameName(self):
        return self._gameName

    def set_gameName(self, gameName):
        self._gameName = gameName

    def get_tagLine(self):
        return self._tagLine

    def set_tagLine(self, tagLine):
        self._tagLine = tagLine

    def get_profileIconId(self):
        return self._profileIconId

    def set_profileIconId(self, profileIconId):
        self._profileIconId = profileIconId

    def get_summonerLevel(self):
        return self._summonerLevel

    def set_summonerLevel(self, summonerLevel):
        self._summonerLevel = summonerLevel

    def get_tier(self):
        return self._tier

    def set_tier(self, tier):
        self._tier = tier

    def get_rank(self):
        return self._rank

    def set_rank(self, rank):
        self._rank = rank

    def __str__(self):
        return (f"User: id={self._id}, puuid={self._puuid}, token={self._token}, "
                f"gameName={self._gameName}, tagLine={self._tagLine}, "
                f"profileIconId={self._profileIconId}, summonerLevel={self._summonerLevel}, "
                f"tier={self._tier}, rank={self._rank}")

    @staticmethod
    def umwandlung(dic: dict):
        obj = User(
            id=dic.get('id', 0),
            puuid=dic.get('puuid', ''),
            token=dic.get('token', ''),
            gameName=dic.get('gameName', ''),
            tagLine=dic.get('tagLine', ''),
            profileIconId=dic.get('profileIconId', 0),
            summonerLevel=dic.get('summonerLevel', 0),
            tier=dic.get('tier', 'UNRANKED'),
            rank=dic.get('rank', '')
        )
        return obj
