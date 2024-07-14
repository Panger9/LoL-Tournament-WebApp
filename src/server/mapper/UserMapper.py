from server.bo.User import User
from server.mapper.Mapper import Mapper

class UserMapper(Mapper):

    def __init__(self):
        super().__init__()

    def find_all(self):
        
        cursor = self._cnx.cursor()
        cursor.execute('SELECT * FROM users')
        tuples = cursor.fetchall()
        result = []

        for (id,sum_name, tag_line, token) in tuples:
            user = User(id, sum_name, tag_line, token)
            result.append(user)

        self._cnx.commit()  
        cursor.close()  

        return result

    def find_by_id(self, id):
        # Logik zum Auslesen eines Users anhand der ID
        pass

    def insert(self, user):
        # Logik zum Einfügen eines neuen Users in die Datenbank
        pass

    def update(self, user):
        # Logik zum Aktualisieren eines vorhandenen Users
        pass

    def delete(self, user):
        # Logik zum Löschen eines Users
        pass