from server.bo.User import User
from server.bo.Team import Team
from server.bo.Turnier import Turnier

from server.mapper.UserMapper import UserMapper
from server.mapper.TeamMapper import TeamMapper
from server.mapper.TurnierMapper import TurnierMapper
from server.mapper.UserTurnierMapper import UserTurnierMapper
from server.mapper.UserTeamMapper import UserTeamMapper

from server.ApiIntegration.RiotApi import RiotAPIIntegration

import string, random

class ApplicationLogic(object):
  def __init__(self):
    self.riot_api = RiotAPIIntegration()
    

  def create_token(self):
      # Erstellt eine Zeichenfolge, die aus Groß- und Kleinbuchstaben sowie Zahlen besteht
      characters = string.ascii_letters + string.digits
      # Wählt zufällig 12 Zeichen aus der Zeichenfolge aus
      token = ''.join(random.choice(characters) for _ in range(12))
      return token

  """
  Im folgenden werden alle Funktionen aufgeführt, welche Daten von der Datenbank abrufen.
  """

#------------------------------------------------------------------------------------------------------------------------------------------------
# USER
#------------------------------------------------------------------------------------------------------------------------------------------------
  def get_all_users(self):
    with UserMapper() as mapper:
      return mapper.find_all()
  
  def get_user_by_id(self, id):
    with UserMapper() as mapper:
      return mapper.find_by_id(id)
  
  def get_user_by_token(self, token):
    with UserMapper() as mapper:
      return mapper.find_by_token(token)
  
  def get_user_by_turnier(self, turnier_id):
     with UserMapper() as mapper:
        return mapper.find_by_turnier(turnier_id)
     
  def get_user_by_team(self, team_id):
     with UserMapper() as mapper:
        return mapper.find_by_team(team_id)
  
  def get_user_by_team_and_turnier(self, turnier_id):
      result = []
      all_teams = self.get_team_by_turnier_id(turnier_id)
      for team in all_teams:
          team_users = []
          users = self.get_user_by_team(team._id)
          for user in users:
              user_info = self.get_playerinfo_important(user._sum_name, user._tag_line)
              team_users.append(user_info)
          result.append(team_users)
      return result



    
  def create_user(self, user):
    log = ApplicationLogic()
    token = log.create_token()
    user.set_token(token)
    
    with UserMapper() as mapper:
      return mapper.insert(user)
    
  def update_user(self, user):
     with UserMapper() as mapper:
        return mapper.update(user)
     
  def delete_user(self, token):
     with UserMapper() as mapper:
        return mapper.delete(token)

#------------------------------------------------------------------------------------------------------------------------------------------------
# TURNIERE
#------------------------------------------------------------------------------------------------------------------------------------------------

  def get_all_turniere(self):
    with TurnierMapper() as mapper:
      return mapper.find_all()

  def get_turnier_by_id(self, id):
    with TurnierMapper() as mapper:
      return mapper.find_by_id(id)
    
  def create_turnier(self, turnier):
     with TurnierMapper() as mapper:
        return mapper.insert(turnier)
     
  def update_turnier(self, turnier):
     with TurnierMapper() as mapper:
        return mapper.update(turnier) 
     
  def delete_turnier(self, id):
     with TurnierMapper() as mapper:
        return mapper.delete(id) 
     
#------------------------------------------------------------------------------------------------------------------------------------------------
# TEAMS
#------------------------------------------------------------------------------------------------------------------------------------------------

  def get_all_teams(self):
    with TeamMapper() as mapper:
      return mapper.find_all()

  def get_team_by_id(self, id):
    with TeamMapper() as mapper:
      return mapper.find_by_id(id)
  
  def get_team_by_turnier_id(self, turnier_id):
     with TeamMapper() as mapper:
        return mapper.find_by_turnier(turnier_id)
    
  def create_team(self, team):
     with TeamMapper() as mapper:
        return mapper.insert(team)

  def update_team(self, team):
     with TeamMapper() as mapper:
        return mapper.update(team) 
     
  def delete_team(self, id):
     with TeamMapper() as mapper:
        return mapper.delete(id) 
     
  def delete_teams_from_turnier(self, turnier_id):
     with TeamMapper() as mapper:
        return mapper.delete_from_turnier(turnier_id) 
     
  
#------------------------------------------------------------------------------------------------------------------------------------------------
# USER-TURNIER
#------------------------------------------------------------------------------------------------------------------------------------------------

  def get_all_user_turnier_entries(self):
     with UserTurnierMapper() as mapper:
        return mapper.find_all()

  def create_user_turnier_entry(self, user_id, turnier_id):
     with UserTurnierMapper() as mapper:
        return mapper.insert(user_id, turnier_id)
     
  def delete_user_from_turnier(self, user_id, turnier_id):
     with UserTurnierMapper() as mapper:
        return mapper.delete(user_id, turnier_id)
     
#------------------------------------------------------------------------------------------------------------------------------------------------
# USER-TEAM
#------------------------------------------------------------------------------------------------------------------------------------------------

  def get_all_user_team_entries(self):
     with UserTeamMapper() as mapper:
        return mapper.find_all()

  def create_user_team_entry(self, user_id, team_id):
     with UserTeamMapper() as mapper:
        return mapper.insert(user_id, team_id)
     
  def delete_user_from_team(self, user_id, team_id):
     with UserTeamMapper() as mapper:
        return mapper.delete(user_id, team_id)

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
      response_all = {}

      # Erstes Response-Dictionary unverändert hinzufügen
      response1 = log.get_playerinfo1(sumName, tagLine)
      response_all.update(response1)

      # Zweites Response-Dictionary filtern und hinzufügen
      response2 = log.get_playerinfo2(response1['puuid'])
      filtered_response2 = {key: response2[key] for key in ['id', 'profileIconId', 'summonerLevel']}
      response_all.update(filtered_response2)

      # Drittes Response-Dictionary (Liste von Dictionaries) filtern und hinzufügen
      response3 = log.get_playerinfo3(response2['id'])
      keys_to_keep = ['queueType', 'tier', 'rank', 'leaguePoints', 'wins', 'losses']
      filtered_response3 = [{key: item[key] for key in keys_to_keep if key in item} for item in response3]
      response_all['rankedInfo'] = filtered_response3

      return response_all

  def get_playerinfo_important(self, sumName, tagLine):
    log = ApplicationLogic()
    response_all = {}

    # Erstes Response-Dictionary unverändert hinzufügen
    response1 = log.get_playerinfo1(sumName, tagLine)
    response_all.update(response1)

    # Zweites Response-Dictionary filtern und hinzufügen
    response2 = log.get_playerinfo2(response1['puuid'])
    filtered_response2 = {key: response2[key] for key in ['id', 'profileIconId', 'summonerLevel']}
    response_all.update(filtered_response2)

    # Drittes Response-Dictionary (Liste von Dictionaries) filtern und hinzufügen
    response3 = log.get_playerinfo3(response2['id'])
    keys_to_keep = ['queueType', 'tier', 'rank', 'leaguePoints', 'wins', 'losses']
    
    # Suche nach dem gewünschten queueType
    ranked_info = None
    for item in response3:
        if item.get('queueType') == 'RANKED_SOLO_5x5':
            ranked_info = {key: item[key] for key in keys_to_keep if key in item}
            break
    
    # Falls "RANKED_SOLO_5x5" nicht gefunden wurde, nach "RANKED_FLEX_SR" suchen
    if ranked_info is None:
        for item in response3:
            if item.get('queueType') == 'RANKED_FLEX_SR':
                ranked_info = {key: item[key] for key in keys_to_keep if key in item}
                break
    
    # Falls ein passendes Dictionary gefunden wurde, hinzufügen
    if ranked_info:
        response_all.update(ranked_info)

    return response_all
  

  """
  Im folgenden werden alle Funktionen aufgeführt, welche Daten von der Datenbank abrufen UND von der API fetchen.
  """

  def login(self, token):
      log = ApplicationLogic()
      _user = log.get_user_by_token(token)

      if _user is None:
          # Fall 1: Der User ist der Datenbank unbekannt
          response = ('Keinen User gefunden', 404)  # 404 Not Found
      else:
          try:
              # Versucht, Spielerinformationen zu erhalten
              player_info = log.get_playerinfo_important(_user._sum_name, _user._tag_line)
              if player_info:
                  # Fall 3: Der User ist in der Datenbank und die Anfrage hat funktioniert
                  response = (player_info, 200)  # 200 OK
              else:
                  # Falls die Anfrage erfolgreich ist, aber keine Daten zurückkommen
                  response = ('Keine Spielerinformationen gefunden', 204)  # 204 No Content
          except Exception as e:
              # Fall 2: Der User ist in der Datenbank, aber die Anfrage an die externe API hat nicht funktioniert
              response = ('Token vorhanden, Anfrage an Riot fehlgeschlagen', 502)  # 502 Bad Gateway

      return response
  
def register(self):
   pass

    

