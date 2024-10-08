from server.bo.Turnier import Turnier
from server.mapper.Mapper import Mapper


class TurnierMapper(Mapper):
    def find_all(self):
        cursor = self._cnx.cursor()
        cursor.execute("SELECT * FROM turniere")
        tuples = cursor.fetchall()
        result = []

        for (id, name, team_size, turnier_owner, start_date, access, phase) in tuples:
            turnier = Turnier(id, name, team_size, turnier_owner, start_date, access, phase)
            result.append(turnier)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_id(self, id):
        cursor = self._cnx.cursor()
        cursor.execute(f"SELECT * FROM turniere WHERE id={id}")
        tuple = cursor.fetchone()
        if tuple:
            (id, name, team_size, turnier_owner, start_date, access, phase) = tuple
            result = Turnier(id, name, team_size, turnier_owner, start_date, access, phase)
        else:
            result = None

        self._cnx.commit()
        cursor.close()

        return result
    
    def find_by_owner_id(self, turnier_owner):
        cursor = self._cnx.cursor()
        cursor.execute(f"SELECT * FROM turniere WHERE turnier_owner={turnier_owner}")
        tuples = cursor.fetchall()
        result = []

        for (id, name, team_size, turnier_owner, start_date, access, phase) in tuples:
            turnier = Turnier(id, name, team_size, turnier_owner, start_date, access, phase)
            result.append(turnier)

        self._cnx.commit()
        cursor.close()

        return result

    def insert(self, turnier):
        cursor = self._cnx.cursor()

        cursor.execute(
            "INSERT INTO turniere (id, name, team_size, turnier_owner, start_date, access, phase) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (turnier.get_id(), turnier.get_name(), turnier.get_team_size(), turnier.get_turnier_owner(), 
             turnier.get_start_date(), turnier.get_access(), turnier.get_phase())
        )

        self._cnx.commit()
        cursor.close()

        return turnier

    def update(self, turnier):
        cursor = self._cnx.cursor()
        cursor.execute(
            "UPDATE turniere SET name = %s, team_size = %s, turnier_owner = %s, start_date = %s, access = %s, phase = %s "
            "WHERE id = %s",
            (turnier.get_name(), turnier.get_team_size(), turnier.get_turnier_owner(), turnier.get_start_date(), 
             turnier.get_access(), turnier.get_phase(), turnier.get_id())
        )

        self._cnx.commit()
        cursor.close()

        return turnier

    def delete(self, id):
        cursor = self._cnx.cursor()
        cursor.execute(f"DELETE FROM turniere WHERE id={id}")

        self._cnx.commit()
        cursor.close()
