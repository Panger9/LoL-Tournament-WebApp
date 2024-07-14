class User():

  def __init__(self, id, sum_name, tag_line, token):
    self._id = id
    self._sum_name = sum_name
    self._tag_line = tag_line
    self._token = token

  def get_id(self):
    return self._id
  
  def set_id(self, id):
    self._id = id

  def get_sum_name(self):
    return self._sum_name
  
  def set_sum_name(self, sum_name):
    self._sum_name = sum_name

  def get_tag_line(self):
    return self._tag_line
  
  def set_tag_line(self, tag_line):
    self._tag_line = tag_line

  def get_token(self):
    return self._token
  
  def set_token(self, token):
    self._token = token

  def __str__(self):
    return f"User: {self._id}, {self._sum_name}, {self._tag_line}, {self._token}"

  @staticmethod
  def umwandlung(dic:dict):
    obj = User()
    obj.set_id(dic['id'])
    obj.set_sum_name(dic['sum_name'])
    obj.set_tag_line(dic['tag_line'])
    obj.set_token(dic['token'])
    return obj