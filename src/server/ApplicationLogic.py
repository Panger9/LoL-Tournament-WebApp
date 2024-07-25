from server.bo.User import User
from server.bo.Team import Team
from server.bo.Turnier import Turnier

from server.mapper.UserMapper import UserMapper
from server.mapper.TeamMapper import TeamMapper
from server.mapper.TurnierMapper import TurnierMapper

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
    
  def create_user(self, user):
    log = ApplicationLogic()
    token = log.create_token()
    user.set_token(token)
    
    with UserMapper() as mapper:
      return mapper.insert(user)
    
  def update_user(self, user):
     with UserMapper() as mapper:
        return mapper.update(user)
     
  def delete_user(self, id):
     with UserMapper() as mapper:
        return mapper.delete(id)

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
    
  def create_team(self, team):
     with TeamMapper() as mapper:
        return mapper.insert(team)

  def update_team(self, team):
     with TeamMapper() as mapper:
        return mapper.update(team) 
     
  def delete_team(self, id):
     with TeamMapper() as mapper:
        return mapper.delete(id) 
    

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
              player_info = log.get_playerinfo_all(_user._sum_name, _user._tag_line)
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

    

