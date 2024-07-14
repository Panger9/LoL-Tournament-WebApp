import mysql.connector as connector
import os
from contextlib import AbstractContextManager
from abc import ABC, abstractmethod


class Mapper (AbstractContextManager, ABC):
    # Abstrakte Basisklasse (Superklasse) aller Mapper-Klassen - definiert die Methoden, die in den Subklassen implementiert werden müssen

    def __init__(self):
        self._cnx = None

    def __enter__(self):
    # enter Methode, die aufgerufen wird, sobald das with-Statement beginnt
 
        if os.getenv('GAE_ENV', '').startswith('standard'):
            # Verbindung zwischen Google App Engine und Cloud SQL. App ist im Production Mode im Standard Environment
            self._cnx = connector.connect(user='demo', password='Sopra123',
                          unix_socket='/cloudsql/fullstack-sopra:europe-west3:fullstack-sopra-database',
                          database='smartfridge')
        else:
            # Ausführung des Codes in lokaler Umgebung  - mySQL-Datenbank
            self._cnx = connector.connect(user='root', password='123',
                          host='127.0.0.1',
                          database='lolturnier')
            
            
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # exit Methode, die aufgerufen wird, sobald das with-Statement beendet wird
        self._cnx.close()


    # Abstract Methods - Methoden, die in den Subklassen implementiert werden müssen

    @abstractmethod
    def find_all(self):
        #Auslesen aller Objekte aus der Datenbank
        pass

    @abstractmethod
    def find_by_id(self, id):
        # Auslesen eines Objektes aus der Datenbank anhand der ID
        pass

    @abstractmethod
    def insert(self, object):
        # Einfügen eines Objektes in die Datenbank
        pass

    @abstractmethod
    def update(self, object):
        # Updaten eines in der DB vorhandenen Objektes
        pass

    @abstractmethod
    def delete(self, object):
        # Löschen eines in der DB vorhandenen Objektes
        pass

