import os
import psycopg2
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

# Umgebungsvariablen laden
db   = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
pwd  = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")

# Verbindung herstellen
dsn = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

try:
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"✅ Verbunden mit PostgreSQL\n🔢 Version: {version[0]}")
except psycopg2.Error as e:
    print("❌ Fehler bei der Verbindung zur Datenbank:")
    print(e)
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
