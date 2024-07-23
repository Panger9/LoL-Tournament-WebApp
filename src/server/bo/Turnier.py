class Turnier():
    def __init__(self, id=0, name='', team_size=0):
        self._id = id
        self._name = name
        self._team_size = team_size

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_team_size(self):
        return self._team_size

    def set_team_size(self, team_size):
        self._team_size = team_size

    def __str__(self):
        return f"Turnier: {self._id}, name: {self._name}, Team Size: {self._team_size}"

    @staticmethod
    def umwandlung(dic: dict):
        obj = Turnier()
        obj.set_id(dic['id'])
        obj.set_name(dic['name'])
        obj.set_team_size(dic['team_size'])
        return obj