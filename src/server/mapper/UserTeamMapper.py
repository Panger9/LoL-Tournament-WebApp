from server.mapper.Mapper import Mapper

class UserTeamMapper(Mapper):

    def __init__(self):
        super().__init__()

    def find_all(self):
        cursor = self._cnx.cursor()
        query = '''
            SELECT user_id, team_id
            FROM user_team
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        cursor.close()

        # Umwandlung der Abfrageergebnisse in eine Liste von Dictionaries
        result = [{'user_id': user_id, 'team_id': team_id} for (user_id, team_id) in tuples]
        
        return result

    def find_by_id(self, id):
        pass

    def insert(self, user_id, team_id):
        cursor = self._cnx.cursor()
        query = '''
            INSERT INTO user_team (user_id, team_id) 
            VALUES (%s, %s)
        '''
        cursor.execute(query, (user_id, team_id))
        self._cnx.commit()
        cursor.close()
        
        # Rückgabe des eingefügten Eintrags
        return {'user_id': user_id, 'team_id': team_id}

    def update(self, object):
        pass

    def delete(self, user_id, team_id):
        cursor = self._cnx.cursor()
        query = '''
            DELETE FROM user_team 
            WHERE user_id = %s AND team_id = %s
        '''
        cursor.execute(query, (user_id, team_id))
        self._cnx.commit()
        cursor.close()
        
        # Rückgabe der gelöschten Eintrags-IDs
        return {'user_id': user_id, 'team_id': team_id}

