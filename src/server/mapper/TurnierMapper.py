from server.bo.Turnier import Turnier
from server.mapper.Mapper import Mapper


class TurnierMapper(Mapper):
    def find_all(self):

        cursor = self._cnx.cursor()
        cursor.execute("SELECT * FROM turniere")
        tuples = cursor.fetchall()
        result = []

        for (id, name, team_size) in tuples:
            turnier = Turnier(id, name, team_size)
            result.append(turnier)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_id(self, id):
        
        cursor = self._cnx.cursor()
        cursor.execute(f"SELECT * FROM turniere WHERE id={id}")
        tuples = cursor.fetchone()
        result = ''
        
        (id, name, team_size) = tuples
        result = Turnier(id, name, team_size)

        return result

    def insert(self, turnier):
        cursor = self._cnx.cursor()
        cursor.execute("SELECT MAX(id) AS maxid FROM turniere ")
        tuples = cursor.fetchall()

        for (maxid) in tuples:
            if maxid[0] is not None:
               
                turnier.set_id(maxid[0] + 1)
            else:  
                turnier.set_id(1)
        
        cursor.execute(f"INSERT INTO turniere VALUES ({turnier._id},'{turnier._name}',{turnier._team_size})")
        
        self._cnx.commit()  # Bestätigen der Datenbankänderungen
        cursor.close() 

        return turnier

    def update(self, user):
        # Logik zum Aktualisieren eines vorhandenen Users
        pass

    def delete(self, user):
        # Logik zum Löschen eines Users
        pass