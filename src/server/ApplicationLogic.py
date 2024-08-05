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
from datetime import datetime


class ApplicationLogic(object):
  def __init__(self):
    self.riot_api = RiotAPIIntegration()
    

  def create_token(self):
      # Erstellt eine Zeichenfolge, die aus Groß- und Kleinbuchstaben sowie Zahlen besteht
      characters = string.ascii_letters + string.digits
      # Wählt zufällig 12 Zeichen aus der Zeichenfolge aus
      token = ''.join(random.choice(characters) for _ in range(12))
      return token
  
  def validate_datetime_format(self, date_string):
    try:
        datetime.strptime(date_string, '%d.%m.%Y/%H:%M')
        return True
    except ValueError:
        return False

  def rank_mean(self, ranks):
        
        if not isinstance(ranks, list):
            raise ValueError('Parameter "ranks" must be a list')
        if len(ranks) < 1:
            return ''

        rank_to_points = [
            'UNRANKED',
            'IRON IV', 'IRON III', 'IRON II', 'IRON I',
            'BRONZE IV', 'BRONZE III', 'BRONZE II', 'BRONZE I',
            'SILVER IV', 'SILVER III', 'SILVER II', 'SILVER I',
            'GOLD IV', 'GOLD III', 'GOLD II', 'GOLD I',
            'PLATINUM IV', 'PLATINUM III', 'PLATINUM II', 'PLATINUM I',
            'EMERALD IV', 'EMERALD III', 'EMERALD II', 'EMERALD I', 
            'DIAMOND IV', 'DIAMOND III', 'DIAMOND II', 'DIAMOND I',
            'MASTER', 'GRANDMASTER', 'CHALLENGER'
        ]

        all_points = 0

        for rank in ranks:
            if isinstance(rank, int):
                  if rank < 100:
                     rank = 'BRONZE IV'
                  elif 100 <= rank < 300:
                     rank = 'SILVER IV'
                  elif 300 <= rank < 500:
                     rank = 'GOLD IV'
                  elif rank >= 500:
                     rank = 'PLATINUM IV'
            if rank in rank_to_points:
               all_points += rank_to_points.index(rank)
            else:
               raise ValueError(f'Invalid rank: {rank}')  
        

        mean_points = all_points / len(ranks)
        rounded_mean_points = round(mean_points)
        return rank_to_points[rounded_mean_points]
  

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
  
  def get_user_by_puuid(self, puuid):
     with UserMapper() as mapper:
        return mapper.find_by_puuid(puuid)
  
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
          all_player_elo = []
          team_users = [{'team_id': team._id}]
          users = self.get_user_by_team(team._id)
          for user in users:
              user_info = self.get_playerinfo_important_puuid(user['puuid'])
              user_info['role'] = user['role'] 

              #rank mean ermitteln ---------------------------------------------
              if 'tier' in user_info and user_info['tier'] is not None:
                  player_elo = user_info['tier'] + ' ' + user_info['rank']
              else:
                  player_elo = user_info['summonerLevel']
              all_player_elo.append(player_elo)
              #rank mean ermitteln ---------------------------------------------

              team_users.append(user_info)
          mean_team_elo = self.rank_mean(all_player_elo)
          team_users[0]['mean_rank'] = mean_team_elo
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
     
  def delete_user(self, user_id):
     
     user_team_entries = self.get_user_team_entry_by_user_id(user_id)
     user_turnier_entries = self.get_user_turnier_entries_by_user_id(user_id)
     result_user_team = []
     result_user_turnier = []
   
     for user_team in user_team_entries:
        result_user_team.append(self.delete_user_from_team(user_id, user_team['team_id']))
      
     for user_turnier in user_turnier_entries:
        result_user_turnier.append(self.delete_user_from_turnier(user_id, user_turnier['turnier_id']))

     with UserMapper() as mapper:
        user = mapper.delete(user_id)
      
     result = []
     result.append(user)
     result.append(result_user_team)
     result.append(result_user_turnier)

     return result

   

#------------------------------------------------------------------------------------------------------------------------------------------------
# TURNIERE
#------------------------------------------------------------------------------------------------------------------------------------------------

  def get_all_turniere(self):
    with TurnierMapper() as mapper:
      return mapper.find_all()

  def get_turnier_by_id(self, id):
    all_user_in_turnier = self.get_user_by_turnier(id)

    with TurnierMapper() as mapper:
      turnier =  mapper.find_by_id(id)
      slots = str(len(all_user_in_turnier)) + '/' + str(turnier.get_slots())
        
      return {
                'id': turnier.get_id(),
                'name': turnier.get_name(),
                'team_size': turnier.get_team_size(),
                'turnier_owner': turnier.get_turnier_owner(),
                'start_date': turnier.get_start_date(),
                'slots': slots
            }
    
  def get_all_turniere_from_user(self, user_id):
     result = []
     all_user_turnier_entries = self.get_user_turnier_entries_by_user_id(user_id)

     for entry in all_user_turnier_entries:
        turnier = self.get_turnier_by_id(entry['turnier_id'])
        result.append(turnier)
      
     return result
    
  def get_all_turniere_with_slots(self):
     result = []
     all_turniere = self.get_all_turniere()
     for turnier in all_turniere:
        new_turnier = self.get_turnier_by_id(turnier._id)
        result.append(new_turnier)
     return result

  def create_turnier(self, turnier):
        # Validierung von turnier._start_date
        if not self.validate_datetime_format(turnier._start_date):
            raise ValueError('Invalid date format. Expected format: DD.MM.JJJJ/hh:mm')

        with TurnierMapper() as mapper:
            newTurnier = mapper.insert(turnier)

        team = Team(0, turnier._id)
        for x in range(newTurnier._team_size):
            self.create_team(team)

        return newTurnier
     
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
     
  def get_all_teams_from_user(self, user_id):
     result = []
     all_user_team_entries = self.get_user_team_entry_by_user_id(user_id)

     for entry in all_user_team_entries:
        team = self.get_team_by_id(entry['team_id'])
        result.append(team)
      
     return result
    
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
  
  def get_user_turnier_entries_by_user_id(self, user_id):
     with UserTurnierMapper() as mapper:
        return mapper.find_by_user_id(user_id)
     
  def get_user_turnier_entry_by_ids(self, user_id, turnier_id):
     with UserTurnierMapper() as mapper:
        return mapper.find_by_ids(user_id, turnier_id)

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
   
  def get_user_team_entry_by_user_id(self, user_id):
     with UserTeamMapper() as mapper:
        return mapper.find_by_user_id(user_id)
     
  def get_user_team_entry_by_ids(self, user_id, team_id):
     with UserTeamMapper() as mapper:
        return mapper.find_by_ids(user_id, team_id)

  def create_user_team_entry(self, user_id, team_id, role):
     with UserTeamMapper() as mapper:
        return mapper.insert(user_id, team_id, role)
     
  def update_user_team_entry(self, user_id, team_id, role):
     with UserTeamMapper() as mapper:
        return mapper.update(user_id, team_id, role)
     
  def delete_user_from_team(self, user_id, team_id):
     with UserTeamMapper() as mapper:
        return mapper.delete(user_id, team_id)
     
#------------------------------------------------------------------------------------------------------------------------------------------------
# USER-TEAM + USER-TURNIER
#------------------------------------------------------------------------------------------------------------------------------------------------

  def remove_user_from_team_and_turnier(self, user_id, team_id, turnier_id):
     result = []
     response1 = self.delete_user_from_team(user_id, team_id)
     response2 = self.delete_user_from_turnier(user_id, turnier_id)
     
     result.append(response1)
     result.append(response2)
     return result
  
  def add_user_to_team(self, user_id, team_id, turnier_id):
     
     isInTurnier = self.get_user_turnier_entry_by_ids(user_id, turnier_id)
     deleted_entries =  'nichts gelöscht'
     added_entries = []

     if isInTurnier is not None:
       
       all_teams = self.get_team_by_turnier_id(turnier_id)

       for team in all_teams:
          entry = self.get_user_team_entry_by_ids(user_id, team._id)
          if entry is not None:
             deleted_entries = self.remove_user_from_team_and_turnier(user_id, entry['team_id'], turnier_id)
     
     user_team = self.create_user_team_entry(user_id, team_id, 'fill')
     user_turnier = self.create_user_turnier_entry(user_id, turnier_id)
     added_entries.append(user_team)
     added_entries.append(user_turnier)
        
     return ['DELETED: ',deleted_entries, 'ADDED', added_entries]
  

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
  
  def get_playerinfo1_with_puuid(self, puuid):
    response = self.riot_api.fetch_puuid_with_puuid(puuid)
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
  
  def get_playerinfo_important_puuid(self, puuid):
    log = ApplicationLogic()
    response_all = {}

    # Erstes Response-Dictionary unverändert hinzufügen
    response1 = log.get_playerinfo1_with_puuid(puuid)
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
              user_id = _user._id
              player_info = log.get_playerinfo_important_puuid(_user._puuid)
              player_info['user_id'] = user_id
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
  

    

