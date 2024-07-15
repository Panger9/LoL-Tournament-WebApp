from flask import Flask, request, send_from_directory
from flask_restx import Api, Resource, fields, Namespace, reqparse
from flask_cors import CORS

from server.ApplicationLogic import ApplicationLogic

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
    'turnier_id': fields.Integer(attribute='_sum_name'),
})

turnier = api.model('turnier', {
    'id': fields.Integer(attribute='_id'),
    'name': fields.String(attribute='_name'),
    'team_size': fields.Integer(attribute='_team_size'),
})

@lolturnier.route('/user')
@lolturnier.response(500, 'Server Error')
class UserListOperations(Resource):

  @lolturnier.marshal_list_with(user)
  def get(self):
    log = ApplicationLogic()
    all_user = log.get_all_users()
    return all_user
  
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
  
if __name__ == '__main__':
    app.run(debug=True)