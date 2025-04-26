import os
import psycopg2
from dotenv import load_dotenv

"""
db_connection_manager als Singleton zur Verwaltung von DB-Verbindungen in Python.
Liest die Einstellungen aus einer .env-Datei und stellt eine Verbindung her.
"""

class db_connection_manager:
    _instance = None

    def __init__(self):
        if db_connection_manager._instance is not None:
            raise Exception("Diese Klasse ist ein Singleton!")
        self._conn = None
        db_connection_manager._instance = self

    @staticmethod
    def get_instance():
        if db_connection_manager._instance is None:
            db_connection_manager()
            db_connection_manager._instance.connect()
        return db_connection_manager._instance

    def connect(self):
        load_dotenv()

        db = os.getenv("POSTGRES_DB")
        user = os.getenv("POSTGRES_USER")
        pwd = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")

        dsn = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

        self._conn = psycopg2.connect(dsn)

    def get_connection(self):
        if self._conn is None:
            self.connect()
        return self._conn
