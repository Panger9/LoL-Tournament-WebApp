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
        
        cursor = self._cnx.cursor()
        cursor.execute(f'SELECT * FROM users WHERE id={id}')
        tuples = cursor.fetchall()

        (id, sum_name, tag_line, token) = tuples[0]
        user = User(id, sum_name, tag_line, token)

        return user
    
    def find_by_token(self, token):
        
        cursor = self._cnx.cursor()
        cursor.execute(f"SELECT * FROM users WHERE token='{token}'")
        tuples = cursor.fetchall()

        try: 
            (id, sum_name, tag_line, token) = tuples[0]
            user = User(id, sum_name, tag_line, token)
            result = user
        except IndexError:
            result = None
        
        return result

    def find_by_turnier(self, turnier_id):
        
        cursor = self._cnx.cursor()

        cursor.execute(f"""SELECT users.id, users.sum_name, users.tag_line, users.token
                            FROM user_turnier
                            JOIN users ON user_turnier.user_id = users.id
                            WHERE user_turnier.turnier_id = {turnier_id}""")
        tuples = cursor.fetchall()
        result = []

        for (id,sum_name, tag_line, token) in tuples:
            user = User(id, sum_name, tag_line, token)
            result.append(user)

        self._cnx.commit()  
        cursor.close()  

        return result

    def find_by_team(self, team_id):
        
        cursor = self._cnx.cursor()

        cursor.execute(f"""SELECT users.id, users.sum_name, users.tag_line, users.token
                            FROM user_team
                            JOIN users ON user_team.user_id = users.id
                            WHERE user_team.team_id = {team_id}""")
        tuples = cursor.fetchall()
        result = []

        for (id,sum_name, tag_line, token) in tuples:
            user = User(id, sum_name, tag_line, token)
            result.append(user)

        self._cnx.commit()  
        cursor.close()  

        return result
        

    def insert(self, user):
        
        cursor = self._cnx.cursor()
        cursor.execute("SELECT MAX(id) AS maxid FROM users ")
        tuples = cursor.fetchall()

        for (maxid) in tuples:
            if maxid[0] is not None:
               
                user.set_id(maxid[0] + 1)
            else:  
                user.set_id(1)
        
        cursor.execute(f"INSERT INTO users VALUES ({user._id},'{user._sum_name}','{user._tag_line}','{user._token}')")
        
        self._cnx.commit()  
        cursor.close() 

        return user

    def update(self, user):

        cursor = self._cnx.cursor()        
        cursor.execute("UPDATE users SET sum_name = %s, tag_line = %s WHERE id = %s",(user._sum_name, user._tag_line, user._id))
        
        self._cnx.commit()  
        cursor.close() 

        return user

    def delete(self, token):
        
        cursor = self._cnx.cursor()        
        cursor.execute(f"DELETE FROM users WHERE token='{token}'")
        
        self._cnx.commit()  
        cursor.close() 


        