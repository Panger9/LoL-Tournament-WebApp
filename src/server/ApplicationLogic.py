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
    
  def get_puuid(self, sumName, tagLine):
    response = self.riot_api.fetch_puuid(sumName, tagLine)
    return response


