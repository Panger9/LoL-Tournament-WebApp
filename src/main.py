from flask import Flask, request, send_from_directory
from flask_restx import Api, Resource, fields, Namespace, reqparse
from flask_cors import CORS

from server.ApplicationLogic import ApplicationLogic

from server.bo.User import User
from server.bo.Team import Team
from server.bo.Turnier import Turnier

# Flask App muss erstellt werden
app = Flask(__name__)

# Cross-Origin Resource Sharing, um Anfragen von diversen Ursprüngen zu akzeptieren.
CORS(app, resources=r'/lolturnier/*')

# Modell, welches unserere Datenstruktur beschreibt, auf deren Basis Clients und Server Daten austauschen. Grundlage ist flask-restx
api = Api(app, version='0.5', title='lolturnier API', description='verwalte Anfragen an das lolturnier Backend')

# Namespace für die Strukturierung der API, alle wichtigen Operatoren werden unter dem Präfix lolturnier zusammengefasst
lolturnier = api.namespace('lolturnier', description='Funktionen des SmartFridges')

# BusinessObject dient als Basisklasse, auf der die weiteren Strukturen aufsetzen.
user = api.model('user', {
    'id': fields.Integer(attribute='_id'),
    'sum_name': fields.String(attribute='_sum_name'),
    'tag_line': fields.String(attribute='_tag_line'),
    'token': fields.String(attribute='_token'),
})

team = api.model('team', {
    'id': fields.Integer(attribute='_id'),
    'turnier_id': fields.Integer(attribute='_turnier_id'),
})

turnier = api.model('turnier', {
    'id': fields.Integer(attribute='_id'),
    'name': fields.String(attribute='_name'),
    'team_size': fields.Integer(attribute='_team_size'),
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
        
        
@lolturnier.route('/user-by-id/<int:id>')
@lolturnier.response(500, 'Server Error')
class UserOperationsId(Resource):

  @lolturnier.marshal_with(user)
  def get(self, id):
    log = ApplicationLogic()
    _user = log.get_user_by_id(id)

    return _user

@lolturnier.route('/user-by-token/<string:token>')
@lolturnier.response(500, 'Server Error')
class UserOperationsToken(Resource):

  @lolturnier.marshal_with(user)
  def get(self, token):
    log = ApplicationLogic()
    _user = log.get_user_by_token(token)
    return _user
  
@lolturnier.route('/user-login/<string:token>')
@lolturnier.response(500, 'Server Error')
class UserOperationsLogin(Resource):
   
   def get(self, token):
      log = ApplicationLogic()
      response = log.login(token)
      return response
   

   


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

        if proposal is not None:
           _turnier = log.create_turnier(proposal)
           return _turnier, 200
        else:
           return "Proposal ist leer", 500
      
      
@lolturnier.route('/turnier-by-id/<int:id>')
@lolturnier.response(500, 'Server Error')
class TurnierOperations(Resource):
   
   @lolturnier.marshal_with(turnier)
   def get(self, id):
      log = ApplicationLogic()
      response = log.get_turnier_by_id(id)
      return response
   
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
        
@lolturnier.route('/team-by-id/<int:id>')
@lolturnier.response(500, 'Server Error')
class TeamOperations(Resource):
   
    @lolturnier.marshal_with(team)
    def get(self, id):
      log = ApplicationLogic()
      response = log.get_team_by_id(id)
      return response

#------------------------------------------------------------------------------------------------------------------------------------------------
# Anfragen an die Riot API
#------------------------------------------------------------------------------------------------------------------------------------------------
  
@lolturnier.route('/riot/get-playerinfo1/<string:sumName>/<string:tagLine>')
class RiotAPIa(Resource):
    def get(self, sumName, tagLine):
        log = ApplicationLogic()
        return log.get_playerinfo1(sumName, tagLine)
    
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

@lolturnier.route('/riot/get-playerinfo_all/<string:sumName>/<string:tagLine>')
class RiotAPId(Resource):
    def get(self, sumName, tagLine):
        log = ApplicationLogic()
        return log.get_playerinfo_all(sumName, tagLine)

#------------------------------------------------------------------------------------------------------------------------------------------------
# Anfragen an die Riot API und die Datenbank
#------------------------------------------------------------------------------------------------------------------------------------------------




if __name__ == '__main__':
    app.run(debug=True)