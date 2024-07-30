from server.mapper.Mapper import Mapper

class UserTurnierMapper(Mapper):

    def __init__(self):
        super().__init__()

    def find_all(self):
        cursor = self._cnx.cursor()
        query = '''
            SELECT user_id, turnier_id
            FROM user_turnier
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        cursor.close()

        # Umwandlung der Abfrageergebnisse in eine Liste von Dictionaries
        result = [{'user_id': user_id, 'turnier_id': turnier_id} for (user_id, turnier_id) in tuples]
        
        return result
    
    def find_by_id(self):
        pass

    def find_by_user_id(self, user_id):
        cursor = self._cnx.cursor()
        query = f'''
            SELECT user_id, turnier_id
            FROM user_turnier
            WHERE user_id={user_id}
        '''
        cursor.execute(query)
        tuples = cursor.fetchall()
        cursor.close()

        # Umwandlung der Abfrageergebnisse in eine Liste von Dictionaries
        result = [{'user_id': user_id, 'turnier_id': turnier_id} for (user_id, turnier_id) in tuples]
        
        return result
    
    def find_by_ids(self, user_id, turnier_id):
        cursor = self._cnx.cursor()
        query = '''
            SELECT user_id, turnier_id
            FROM user_turnier
            WHERE user_id=%s AND turnier_id=%s
        '''
        cursor.execute(query, (user_id, turnier_id))
        row = cursor.fetchone()
        cursor.close()

        # Umwandlung des Abfrageergebnisses in ein Dictionary
        if row:
            result = {'user_id': row[0], 'turnier_id': row[1]}
        else:
            result = None

        return result

    def insert(self, user_id, turnier_id):
        cursor = self._cnx.cursor()
        query = '''
            INSERT INTO user_turnier (user_id, turnier_id) 
            VALUES (%s, %s)
        '''
        cursor.execute(query, (user_id, turnier_id))
        self._cnx.commit()
        cursor.close()
        
        # Rückgabe des eingefügten Eintrags
        return {'user_id': user_id, 'turnier_id': turnier_id}

    def update(self, object):
        pass

    def delete(self, user_id, turnier_id):
        cursor = self._cnx.cursor()
        query = '''
            DELETE FROM user_turnier 
            WHERE user_id = %s AND turnier_id = %s
        '''
        cursor.execute(query, (user_id, turnier_id))
        self._cnx.commit()
        cursor.close()
        
        # Rückgabe der gelöschten Eintrags-IDs
        return {'user_id': user_id, 'turnier_id': turnier_id}
