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

        for (id, puuid, token) in tuples:
            user = User(id, puuid, token)
            result.append(user)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_id(self, id):
        cursor = self._cnx.cursor()
        cursor.execute(f'SELECT * FROM users WHERE id={id}')
        tuples = cursor.fetchall()

        (id, puuid, token) = tuples[0]
        user = User(id, puuid, token)

        return user
    
    def find_by_token(self, token):
        cursor = self._cnx.cursor()
        cursor.execute(f"SELECT * FROM users WHERE token='{token}'")
        tuples = cursor.fetchall()

        try:
            (id, puuid, token) = tuples[0]
            user = User(id, puuid, token)
            result = user
        except IndexError:
            result = None

        self._cnx.commit()  
        cursor.close()

        return result
    
    def find_by_puuid(self, puuid):
        cursor = self._cnx.cursor()
        cursor.execute(f"SELECT * FROM users WHERE puuid='{puuid}'")
        tuples = cursor.fetchall()

        if tuples:
            (id, puuid, token) = tuples[0]
            user = User(id, puuid, token)
            result = user
        else:
            result = None

        self._cnx.commit()  
        cursor.close()  
        
        return result

    def find_by_turnier(self, turnier_id):
        cursor = self._cnx.cursor()
        cursor.execute(f"""SELECT users.id, users.puuid, users.token
                            FROM user_turnier
                            JOIN users ON user_turnier.user_id = users.id
                            WHERE user_turnier.turnier_id = {turnier_id}""")
        tuples = cursor.fetchall()
        result = []

        for (id, puuid, token) in tuples:
            user = User(id, puuid, token)
            result.append(user)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_team(self, team_id):
        cursor = self._cnx.cursor()
        cursor.execute(f"""SELECT users.id, users.puuid, users.token, user_team.role
                            FROM user_team
                            JOIN users ON user_team.user_id = users.id
                            WHERE user_team.team_id = {team_id}""")
        tuples = cursor.fetchall()
        result = []

        for (id, puuid, token, role) in tuples:
            user = {'id': id, 'puuid': puuid, 'token': token, 'role': role}
            result.append(user)

        self._cnx.commit()
        cursor.close()

        return result

    def insert(self, user):
        cursor = self._cnx.cursor()
        cursor.execute("SELECT MAX(id) AS maxid FROM users")
        tuples = cursor.fetchall()

        for (maxid) in tuples:
            if maxid[0] is not None:
                user.set_id(maxid[0] + 1)
            else:
                user.set_id(1)
        
        cursor.execute(f"INSERT INTO users VALUES ({user._id},'{user._puuid}','{user._token}')")
        
        self._cnx.commit()
        cursor.close()

        return user

    def update(self, user):
        cursor = self._cnx.cursor()
        cursor.execute("UPDATE users SET puuid = %s WHERE id = %s", (user._puuid, user._id))
        
        self._cnx.commit()
        cursor.close()

        return user

    def delete(self, user_id):

        cursor = self._cnx.cursor()
        cursor.execute(f"DELETE FROM users WHERE id='{user_id}'")
        
        self._cnx.commit()
        cursor.close()

        return {"deleted_user_id": user_id}