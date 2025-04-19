# Basis­image mit Python
FROM python:3.12

# Arbeits­verzeichnis im Container
WORKDIR /app

# System­bibliotheken für psycopg2 (Postgres‑Adapter)
RUN apt-get update \
 && apt-get install -y build-essential libpq-dev --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# Python‑Dependencies installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Deinen gesamten Code ins Image kopieren
COPY . .

# (Optional) Port freigeben
EXPOSE 8000

# Standard­kommando
CMD ["python", "scr/main.py"]
