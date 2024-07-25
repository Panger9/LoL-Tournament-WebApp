from server.bo.Team import Team
from server.mapper.Mapper import Mapper


class TeamMapper(Mapper):
    def find_all(self):

        cursor = self._cnx.cursor()
        cursor.execute("SELECT * FROM teams")
        tuples = cursor.fetchall()
        result = []

        for (id, turnier_id) in tuples:
            team = Team(id, turnier_id)
            result.append(team)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_id(self, id):

        cursor = self._cnx.cursor()
        cursor.execute(f"SELECT * FROM teams WHERE id={id}")
        tuples = cursor.fetchone()
        result = ''

        (id, turnier_id) = tuples
        result = Team(id, turnier_id)


        self._cnx.commit()
        cursor.close()

        return result

    def insert(self, team):
        cursor = self._cnx.cursor()
        cursor.execute("SELECT MAX(id) AS maxid FROM teams ")
        tuples = cursor.fetchall()

        for (maxid) in tuples:
            if maxid[0] is not None:
               
                team.set_id(maxid[0] + 1)
            else:  
                team.set_id(1)
        
        cursor.execute(f"INSERT INTO teams VALUES ({team._id},{team._turnier_id})")
        
        self._cnx.commit()  # Bestätigen der Datenbankänderungen
        cursor.close() 

        return team

    def update(self, team):

        cursor = self._cnx.cursor()        
        cursor.execute("UPDATE teams SET turnier_id = %s WHERE id = %s",(team._turnier_id, team._id))
        
        self._cnx.commit()  
        cursor.close() 

        return team

    def delete(self, id):
        
        cursor = self._cnx.cursor()        
        cursor.execute(f"DELETE FROM teams WHERE id={id}")
        
        self._cnx.commit()  
        cursor.close() 