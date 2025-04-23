# DIS Übung (PostgreSQL + Python)

---

## Requirements

- Docker
- Python (≥ 3.9 recommended)  
- [Poetry](https://python-poetry.org/docs/#installation)

---

## 📦 Setup Guide

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 2. Create `.env` file

```env
POSTGRES_DB=dis-db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

---

### 3. Start PostgreSQL with Docker

```bash
docker-compose up -d
```

You can check logs with:

```bash
docker-compose logs -f
```

---

### 4. Install Python dependencies

```bash
poetry install
```

---

### 5. Run test script

```bash
poetry run python scr/exercise2/main.py
```

You should see a success message with PostgreSQL version info.

---

## ✅ Common Commands

| Task                          | Command                                      |
|------------------------------|----------------------------------------------|
| Start DB                     | `docker-compose up -d`                       |
| Stop DB                      | `docker-compose down`                        |
| Connect to DB (psql)         | `docker exec -it dis_docker_container psql -U postgres -d dis-db` |
| Format code                  | `poetry run black .`                         |
| Run main.py                  | `poetry run python scr/exercise2/main.py`   |

---

## 🛠️ Notes

- Data is persisted in a Docker volume named `db-data`.
- To completely reset the DB (wipe everything):

```bash
docker-compose down -v
```
