import os
import psycopg2
from time import sleep
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

# Optional: auf Datenbank warten (z.B. bei Docker-Compose)
sleep(5)

# Umgebungsvariablen lesen
db   = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
pwd  = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("DB_HOST", "dis")
port = os.getenv("DB_PORT", "5432")

# DSN-String zusammenbauen
dsn = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
print(f"-----------postgresql://{user}:{pwd}@{host}:{port}/{db} {dsn}")

# Verbindung herstellen
conn = psycopg2.connect(dsn)

# Abfrage zum Testen
cur = conn.cursor()
cur.execute("SELECT version();")
print("Postgres Version:", cur.fetchone())
print("------------------ ich bin verbunden -----------")

cur.close()
conn.close()
