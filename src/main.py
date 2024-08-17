from flask import Flask, request, send_from_directory
from flask_restx import Api, Resource, fields, Namespace, reqparse, abort
from flask_cors import CORS

from server.ApplicationLogic import ApplicationLogic

from server.bo.User import User
from server.bo.Team import Team
from server.bo.Turnier import Turnier

from datetime import datetime

# Flask App muss erstellt werden
app = Flask(__name__)

# Cross-Origin Resource Sharing, um Anfragen von diversen Ursprüngen zu akzeptieren.
CORS(app, resources=r'/lolturnier/*')

# Modell, welches unserere Datenstruktur beschreibt, auf deren Basis Clients und Server Daten austauschen. Grundlage ist flask-restx
api = Api(app, version='0.5', title='lolturnier API', description='verwalte Anfragen an das lolturnier Backend')

# Namespace für die Strukturierung der API, alle wichtigen Operatoren werden unter dem Präfix lolturnier zusammengefasst
lolturnier = api.namespace('lolturnier', description='Funktionen der Tournament App')

# BusinessObject dient als Basisklasse, auf der die weiteren Strukturen aufsetzen.
user = api.model('user', {
    'id': fields.Integer(attribute='_id'),
    'puuid': fields.String(attribute='_puuid'),
    'token': fields.String(attribute='_token'),
    'gameName': fields.String(attribute='_gameName'),
    'tagLine': fields.String(attribute='_tagLine'),
    'profileIconId': fields.Integer(attribute='_profileIconId'),
    'summonerLevel': fields.Integer(attribute='_summonerLevel'),
    'tier': fields.String(attribute='_tier'),
    'rank': fields.String(attribute='_rank')
})

team = api.model('team', {
    'id': fields.Integer(attribute='_id'),
    'turnier_id': fields.Integer(attribute='_turnier_id'),
})


turnier = api.model('turnier', {
    'id': fields.Integer(attribute='_id'),
    'name': fields.String(attribute='_name'),
    'team_size': fields.Integer(attribute='_team_size'),
    'turnier_owner': fields.Integer(attribute='_turnier_owner'),
    'start_date': fields.String(attribute='_start_date'),
    'access': fields.String(attribute='_access'),  # Neu hinzugefügt
    'phase': fields.String(attribute='_phase')     # Neu hinzugefügt
})


user_team = api.model('user_team', {
   'user_id': fields.Integer,
   'team_id': fields.Integer,
   'role': fields.String

})


#------------------------------------------------------------------------------------------------------------------------------------------------
# Anfragen an die Datenbank
#------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------
# USER
#------------------------------------------------------------------------------------------------------------------------------------------------

@lolturnier.route('/user')
@lolturnier.response(500, 'Server Error')
class UserListOperations(Resource):

    @lolturnier.marshal_list_with(user)
    def get(self):
        log = ApplicationLogic()
        all_user = log.get_all_users()
        return all_user
  
    @lolturnier.expect(user)
    @lolturnier.marshal_with(user)
    def post(self):
        log = ApplicationLogic()
        proposal = User.umwandlung(api.payload)
        if proposal is not None:
           _user = log.create_user(proposal)
           return _user, 200
        else:
           return "Proposal ist leer", 500
        
    @lolturnier.expect(user)
    @lolturnier.marshal_with(user)
    def put(self):
       
        log =ApplicationLogic()
        proposal = User.umwandlung(api.payload)

        if proposal is not None:
           _user = log.update_user(proposal)
           return _user, 200
        else:
           return "Proposal ist leer", 500
        
       
        
@lolturnier.route('/user-by-id/<int:id>')
@lolturnier.response(500, 'Server Error')
class UserOperationsId(Resource):

  @lolturnier.marshal_with(user)
  def get(self, id):
    log = ApplicationLogic()
    _user = log.get_user_by_id(id)

    return _user
  
  def delete(self, id):
    log = ApplicationLogic()
    return log.delete_user(id)
  
@lolturnier.route('/user-by-token/<string:token>')
@lolturnier.response(500, 'Server Error')
class UserOperationsToken(Resource):

  @lolturnier.marshal_with(user)
  def get(self, token):
    log = ApplicationLogic()
    _user = log.get_user_by_token(token)
    return _user
  
@lolturnier.route('/user-by-puuid/<string:puuid>')
@lolturnier.response(500, 'Server Error')
class UserOperationsPuuid(Resource):

  @lolturnier.marshal_with(user)
  def get(self, puuid):
    log = ApplicationLogic()
    _user = log.get_user_by_puuid(puuid)
    if _user is None:
        abort(404, message=f"User with puuid '{puuid}' not found")
    return _user
  
  
@lolturnier.route('/user-by-turnier-id/<int:id>')
@lolturnier.response(500, 'Server Error')
class UserOperationsTurnierId(Resource):

  @lolturnier.marshal_with(user)
  def get(self, id):
    log = ApplicationLogic()
    _user = log.get_user_by_turnier(id)

    return _user
  
@lolturnier.route('/user-by-team-id/<int:id>')
@lolturnier.response(500, 'Server Error')
class UserOperationsTeamId(Resource):


  def get(self, id):
    log = ApplicationLogic()
    _user = log.get_user_by_team(id)

    return _user
  
@lolturnier.route('/user-by-team-and-turnier/<int:turnier_id>')
@lolturnier.response(500, 'Server Error')
class UserOperationsTeamId(Resource):


  def get(self, turnier_id):
    log = ApplicationLogic()
    all_user = log.get_user_by_team_and_turnier(turnier_id)

    return all_user


#------------------------------------------------------------------------------------------------------------------------------------------------
# TURNIERE
#------------------------------------------------------------------------------------------------------------------------------------------------

@lolturnier.route('/turnier')
@lolturnier.response(500, 'Server Error')
class TurnierListOperations(Resource):
   
    @lolturnier.marshal_list_with(turnier)
    def get(self):
        log = ApplicationLogic()
        response = log.get_all_turniere()
        return response
   
    @lolturnier.marshal_with(turnier)
    @lolturnier.expect(turnier)
    def post(self):
        log = ApplicationLogic()
        proposal = Turnier.umwandlung(api.payload)
        print(proposal._start_date)

        if proposal is not None:
           _turnier = log.create_turnier(proposal)
           return _turnier, 200
        else:
           return "Proposal ist leer", 500
        
    @lolturnier.expect(turnier)
    @lolturnier.marshal_with(turnier)
    def put(self):
       
        log =ApplicationLogic()
        proposal = Turnier.umwandlung(api.payload)

        if proposal is not None:
           _turnier = log.update_turnier(proposal)
           return _turnier, 200
        else:
           return "Proposal ist leer", 500
        
@lolturnier.route('/turnier-with-slots')
@lolturnier.response(500, 'Server Error')
class TurnierListOperationsSlots(Resource):

    def get(self):
        log = ApplicationLogic()
        response = log.get_all_turniere_with_slots()
        return response
      
      
@lolturnier.route('/turnier-by-id/<int:id>')
@lolturnier.response(500, 'Server Error')
class TurnierOperations(Resource):
   

   def get(self, id):
      log = ApplicationLogic()
      response = log.get_turnier_by_id(id)
      return response
   
   def delete(self, id):
      log = ApplicationLogic()
      response = log.delete_turnier(id)
      return response
   
@lolturnier.route('/turnier-by-user-id/<int:user_id>')
@lolturnier.response(500, 'server error')
class TurnierListOperationsByUser(Resource):
   

   def get(self, user_id):
      log = ApplicationLogic()
      return log.get_my_tournaments(user_id)
   
#------------------------------------------------------------------------------------------------------------------------------------------------
# TEAMS
#------------------------------------------------------------------------------------------------------------------------------------------------
  
@lolturnier.route('/teams')
@lolturnier.response(500, 'Server Error')
class TeamListOperations(Resource):
   
    @lolturnier.marshal_list_with(team)
    def get(self):
      log = ApplicationLogic()
      response = log.get_all_teams()
      return response
   
    @lolturnier.marshal_with(team)
    @lolturnier.expect(team)
    def post(self):
        log = ApplicationLogic()
        proposal = Team.umwandlung(api.payload)

        if proposal is not None:
           _team = log.create_team(proposal)
           return _team, 200
        else:
           return "Proposal ist leer", 500

    @lolturnier.expect(team)
    @lolturnier.marshal_with(team)
    def put(self):
       
        log =ApplicationLogic()
        proposal = Team.umwandlung(api.payload)

        if proposal is not None:
           _team = log.update_team(proposal)
           return _team, 200
        else:
           return "Proposal ist leer", 500
        
@lolturnier.route('/team-by-id/<int:id>')
@lolturnier.response(500, 'Server Error')
class TeamOperations(Resource):
   
    @lolturnier.marshal_with(team)
    def get(self, id):
      log = ApplicationLogic()
      response = log.get_team_by_id(id)
      return response

    def delete(self, id):
        log = ApplicationLogic()
        response = log.delete_team(id)
        return response

@lolturnier.route('/team-by-turnier-id/<int:turnier_id>')
@lolturnier.response(500, 'Server Error')
class TeamOperationsByTurnier(Resource):
   
    @lolturnier.marshal_list_with(team)
    def get(self, turnier_id):
      log = ApplicationLogic()
      response = log.get_team_by_turnier_id(turnier_id)
      return response

    def delete(self, turnier_id):
        log = ApplicationLogic()
        response = log.delete_teams_from_turnier(turnier_id)
        return response

    
#------------------------------------------------------------------------------------------------------------------------------------------------
# USER-TURNIER
#------------------------------------------------------------------------------------------------------------------------------------------------

@lolturnier.route('/user-turnier')
@lolturnier.response(500, 'Server Error')
class UserTurnierListOperations(Resource):

    def get(self):
        log = ApplicationLogic()
        u = log.get_all_user_turnier_entries()
        return u
    
@lolturnier.route('/user-turnier/<int:user_id>/<int:turnier_id>')
@lolturnier.response(500, 'Server Error')
class UserTurnierOperations(Resource):

    def get(self, user_id, turnier_id):
       log = ApplicationLogic()
       entry = log.get_user_turnier_entry_by_ids(user_id, turnier_id)
       return entry

    def post(self, user_id, turnier_id):
        log = ApplicationLogic()
        all_user = log.create_user_turnier_entry(user_id, turnier_id)
        return all_user
    
    def delete(self, user_id, turnier_id):
       log = ApplicationLogic()
       u = log.delete_user_from_turnier(user_id, turnier_id)
       return u
    
@lolturnier.route('/user-turnier-by-user-id/<int:user_id>')
@lolturnier.response(500, 'Server Error')
class UserTurnierListOperationsByUser(Resource):

    def get(self, user_id):
        log = ApplicationLogic()
        u = log.get_user_turnier_entries_by_user_id(user_id)
        return u
    
#------------------------------------------------------------------------------------------------------------------------------------------------
# USER-TEAM
#------------------------------------------------------------------------------------------------------------------------------------------------

@lolturnier.route('/user-team')
@lolturnier.response(500, 'Server Error')
class UserTeamListOperations(Resource):

    def get(self):
        log = ApplicationLogic()
        u = log.get_all_user_team_entries()
        return u
    
    @lolturnier.expect(user_team)
    def post(self):
        log = ApplicationLogic()
        proposal = api.payload
        all_user = log.create_user_team_entry(proposal['user_id'],proposal['team_id'],proposal['role'])
        return all_user
    
    @lolturnier.expect(user_team)
    def put(self):
        log = ApplicationLogic()
        proposal = api.payload
        all_user = log.update_user_team_entry(proposal['user_id'],proposal['team_id'],proposal['role'])
        return all_user
    
@lolturnier.route('/user-team-by-user-id/<int:user_id>')
@lolturnier.response(500, 'Server Error')
class UserTeamListOperationsA(Resource):

    def get(self, user_id):
       log = ApplicationLogic()
       entry = log.get_user_team_entry_by_user_id(user_id)
       return entry
    
@lolturnier.route('/user-team/<int:user_id>/<int:team_id>')
@lolturnier.response(500, 'Server Error')
class UserTeamOperations(Resource):

    def get(self, user_id, team_id):
       log = ApplicationLogic()
       entry = log.get_user_team_entry_by_ids(user_id, team_id)
       return entry

    def delete(self, user_id, team_id):
       log = ApplicationLogic()
       u = log.delete_user_from_team(user_id, team_id)
       return u

#------------------------------------------------------------------------------------------------------------------------------------------------
# USER-TEAM + USER-TURNIER
#------------------------------------------------------------------------------------------------------------------------------------------------

@lolturnier.route('/user-team-turnier/<int:user_id>/<int:team_id>/<int:turnier_id>')
@lolturnier.response(500, 'Server Error')
class UserTeamTurnierOperations(Resource):

    def delete(self, user_id, team_id, turnier_id):
        log = ApplicationLogic()
        all_deletes = log.remove_user_from_team_and_turnier(user_id, team_id, turnier_id)
        return all_deletes
    
    def post(self, user_id, team_id, turnier_id):
       log = ApplicationLogic()
       return log.add_user_to_team(user_id, team_id, turnier_id)

#------------------------------------------------------------------------------------------------------------------------------------------------
# Anfragen an die Riot API
#------------------------------------------------------------------------------------------------------------------------------------------------
  
@lolturnier.route('/riot/get-playerinfo1/<string:sumName>/<string:tagLine>')
class RiotAPIa(Resource):
    def get(self, sumName, tagLine):
        log = ApplicationLogic()
        return log.get_playerinfo1(sumName, tagLine)
    
@lolturnier.route('/riot/get-playerinfo1-puuid/<string:puuid>')
class RiotAPIf(Resource):
    def get(self, puuid):
        log = ApplicationLogic()
        return log.get_playerinfo1_with_puuid(puuid)
    
@lolturnier.route('/riot/get-playerinfo2/<string:puuid>')
class RiotAPIb(Resource):
    def get(self, puuid):
        log = ApplicationLogic()
        return log.get_playerinfo2(puuid)

@lolturnier.route('/riot/get-playerinfo3/<string:sum_id>')
class RiotAPIc(Resource):
    def get(self, sum_id):
        log = ApplicationLogic()
        return log.get_playerinfo3(sum_id)

@lolturnier.route('/riot/get-playerinfo_important/<string:sumName>/<string:tagLine>')
class RiotAPIe(Resource):
    def get(self, sumName, tagLine):
        log = ApplicationLogic()
        return log.get_playerinfo_important(sumName, tagLine)
    
@lolturnier.route('/riot/get-playerinfo_important-puuid/<string:puuid>')
class RiotAPId(Resource):
    def get(self, puuid):
        log = ApplicationLogic()
        return log.get_playerinfo_important_puuid(puuid)

#------------------------------------------------------------------------------------------------------------------------------------------------
# Anfragen an die Riot API und die Datenbank
#------------------------------------------------------------------------------------------------------------------------------------------------

@lolturnier.route('/user-login/<string:token>')
@lolturnier.response(500, 'Server Error')
class UserOperationsLogin(Resource):
   
   @lolturnier.marshal_with(user)
   def get(self, token):
      log = ApplicationLogic()
      response = log.login(token)
      return response
   
@lolturnier.route('/user-refresh/<int:id>')
@lolturnier.response(500, 'Server Error')
class UserOperationsRefresh(Resource):
   
   @lolturnier.marshal_with(user)
   def get(self, id):
      log = ApplicationLogic()
      response = log.refresh(id)
      return response


if __name__ == '__main__':
    app.run(debug=True)