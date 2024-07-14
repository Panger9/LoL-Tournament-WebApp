class Team():
    def __init__(self, id, turnier_id=0):
        self._id = id
        self._turnier_id = turnier_id

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_turnier_id(self):
        return self._turnier_id

    def set_turnier_id(self, turnier_id):
        self._turnier_id = turnier_id

    def __str__(self):
        return f"Team ID: {self._id}, Turnier ID: {self._turnier_id}"

    @staticmethod
    def umwandlung(dic: dict):
        obj = Team()
        obj.set_id(dic['id'])
        obj.set_turnier_id(dic['turnier_id'])
        return obj