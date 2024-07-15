from server.bo.User import User
from server.bo.Team import Team
from server.bo.Turnier import Turnier

from server.mapper.UserMapper import UserMapper
from server.mapper.TeamMapper import TeamMapper
from server.mapper.TurnierMapper import TurnierMapper

from server.ApiIntegration.RiotApi import RiotAPIIntegration

class ApplicationLogic(object):
  def __init__(self):
    self.riot_api = RiotAPIIntegration()

  def get_all_users(self):
    with UserMapper() as mapper:
      return mapper.find_all()
    

  """
  Im folgenden werden alle Funktionen aufgeführt, welche Daten von der Riot Api fetchen.
  Die fetches, um an die Spielerinformationen zu kommen sind durchnummeriert.
  Um an alle Informationen zu kommen, werden insg. 3 Anfragen benötigt.
  Jede Anfrage ist mit einem Kommentar markiert, der angibt, was die Fetchanfrage ausgibt (Datentyp und key values)
  """


  # dict: {puuid, gameName, tagLine}
  def get_playerinfo1(self, sumName, tagLine):
    response = self.riot_api.fetch_puuid(sumName, tagLine)
    return response

  # dict: {id, accountId, puuid, profileIconId, revisionData, summonerLevel}
  def get_playerinfo2(self, puuid):
    response = self.riot_api.fetch_sum_id(puuid)
    return response

  # Liste mit dicts (nicht vollständig, nur wichtige keys herausgeschrieben): 
  # [{leagueId, queueType, tier, rank, summonerId, leaguePoints, wins, losses},{...},{...}]
  def get_playerinfo3(self, sum_id):
    response = self.riot_api.fetch_playerinfo(sum_id)
    return response
  
  def get_playerinfo_all(self, sumName, tagLine):
    log = ApplicationLogic()
    response_all = []

    # Erstes Response-Dictionary unverändert hinzufügen
    response1 = log.get_playerinfo1(sumName, tagLine)
    response_all.append(response1)

    # Zweites Response-Dictionary filtern und hinzufügen
    response2 = log.get_playerinfo2(response1['puuid'])
    filtered_response2 = {key: response2[key] for key in ['id', 'profileIconId', 'summonerLevel']}
    response_all.append(filtered_response2)

    # Drittes Response-Dictionary (Liste von Dictionaries) filtern und hinzufügen
    response3 = log.get_playerinfo3(response2['id'])
    keys_to_keep = ['queueType', 'tier', 'rank', 'leaguePoints', 'wins', 'losses']
    for item in response3:
        filtered_item = {key: item[key] for key in keys_to_keep if key in item}
        response_all.append(filtered_item)

    return response_all
  
  def get_puuid(self, sumName, tagLine):
    response = self.riot_api.fetch_puuid(sumName, tagLine)
    return response['puuid']
  
  def get_sum_id(self, puuid):
    response = self.riot_api.fetch_sum_id(puuid)
    return response['id']
  
  def get_profile_icon_id(self, puuid):
    response = self.riot_api.fetch_sum_id(puuid)
    return response['profileIconId']
  

  
  
puuid_lanzus = 'hiRYfQC_MlqRjjA3MxduebV_Tpx9crqTssry9YsWz49u5Yba3M94OXO_T8M1WKcmREH68vhPJJ7j-g'
sum_id_lanzus = 'Vp5MLXiZ9RsCvSbvtSl0---yyLcUfrCF3A2WtVLJSKZsfFLR'
# Testdurchläufe in der Konsole
log = ApplicationLogic()
test1 = log.get_playerinfo1('Lanzus73','EUW')
test2 = log.get_playerinfo2(puuid_lanzus)
test3 = log.get_playerinfo3(sum_id_lanzus)

print(test1)
print(test2)
print(test3)

