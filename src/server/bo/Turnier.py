class Turnier:
    def __init__(self, id=0, name='', team_size=0, turnier_owner=0, start_date='', access='public', phase='pre'):
        self._id = id
        self._name = name
        self._team_size = team_size
        self._turnier_owner = turnier_owner
        self._start_date = start_date
        self._access = access
        self._phase = phase

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

    def get_turnier_owner(self):
        return self._turnier_owner

    def set_turnier_owner(self, turnier_owner):
        self._turnier_owner = turnier_owner

    def get_start_date(self):
        return self._start_date

    def set_start_date(self, start_date):
        self._start_date = start_date

    def get_access(self):
        return self._access

    def set_access(self, access):
        self._access = access

    def get_phase(self):
        return self._phase

    def set_phase(self, phase):
        self._phase = phase

    def get_slots(self):
        return self._team_size * 5

    def __str__(self):
        return f"Turnier: {self._id}, Name: {self._name}, Team Size: {self._team_size}, Turnier Owner: {self._turnier_owner}, Start Date: {self._start_date}, Access: {self._access}, Phase: {self._phase}"

    @staticmethod
    def umwandlung(dic: dict):
        obj = Turnier()
        obj.set_id(dic['id'])
        obj.set_name(dic['name'])
        obj.set_team_size(dic['team_size'])
        obj.set_turnier_owner(dic['turnier_owner'])
        obj.set_start_date(dic['start_date'])
        obj.set_access(dic.get('access', 'public'))
        obj.set_phase(dic.get('phase', 'pre'))
        return obj
