## 3.1

### a) Isolation Level in PostgreSQL

**Frage:**  
Öffne eine Verbindung zur Datenbank `dis-2025`.  
Was ist das aktuelle Isolation Level?  
Welche Isolation Levels unterstützt PostgreSQL?

**Lösung:**

```sql
SHOW TRANSACTION ISOLATION LEVEL;
```

**Mögliche Ausgabe:**
```
read committed
```

**Unterstützte Isolation Levels in PostgreSQL:**

- `Read uncommitted` (wird wie `Read committed` behandelt)
- `Read committed` *(Standard)*
- `Repeatable read`
- `Serializable`

---

### b) Tabelle `sheet3` erstellen und mit Daten befüllen

```sql
CREATE TABLE sheet3 (
    id SERIAL PRIMARY KEY,
    name TEXT
);

INSERT INTO sheet3 (name) VALUES
  ('Victor'),
  ('Till'),
  ('Ali');
```

---

### c) Auto-Commit deaktivieren, Transaktion starten und Locks prüfen

1. **Auto-Commit deaktivieren:**  
   In `psql`:

   ```sql
   \set AUTOCOMMIT off
   ```

2. **Transaktion starten und Daten abfragen:**

   ```sql
   BEGIN;

   SELECT *
   FROM sheet3
   WHERE name = 'Till';

   SELECT relation::regclass, mode, granted
   FROM pg_locks
   WHERE relation::regclass = 'sheet3'::regclass;
   ```

3. **Beispielhafte Ausgabe der Locks:**

   | relation | mode            | granted |
   |----------|------------------|---------|
   | sheet3   | AccessShareLock  | true    |

   **Bedeutung:**
   - `AccessShareLock`: Lesesperre – andere Transaktionen können weiterhin lesen, aber nicht exklusiv sperren.

4. **Transaktion abschließen:**

   ```sql
   COMMIT;
   ```

---

### d) Isolation Level auf Serializable setzen und erneut prüfen

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SELECT *
FROM sheet3
WHERE name = 'Till';

SELECT relation::regclass, mode, granted
FROM pg_locks
WHERE relation::regclass = 'sheet3'::regclass;

COMMIT;
```

**Beispielhafte Ausgabe der Locks:**

| relation | mode            | granted |
|----------|------------------|---------|
| sheet3   | AccessShareLock  | true    |
| sheet3   | SIReadLock       | true    |

**Bedeutung:**
- `AccessShareLock`: Lesesperre.
- `SIReadLock`: Spezifische Sperre zur Durchsetzung der **serialisierbaren Isolation** – schützt vor Phantomen und Race Conditions.


---

## 3.2

### d) Welche Aktionen führen zu einem Abbruch (Rollback)?

**Szenario:**  
Zwei Transaktionen (T1 und T2) agieren gleichzeitig und versuchen, sich gegenseitig blockierende Updates durchzuführen.

**Ablauf:**

```text
T1: UPDATE sheet3 SET name = 'x11' WHERE id = 1;
T2: UPDATE sheet3 SET name = 'x22' WHERE id = 2;
T1: UPDATE sheet3 SET name = 'x12' WHERE id = 2;   -- T1 wartet auf Sperre von T2
T2: UPDATE sheet3 SET name = 'x21' WHERE id = 1;   -- Deadlock erkannt
T2: ROLLBACK                                       -- PostgreSQL bricht T2 ab
T1: COMMIT                                         -- T1 kann erfolgreich abschließen
```

**Erklärung:**  
- T1 hält eine Sperre auf Zeile mit `id = 1` und will `id = 2` ändern (blockiert durch T2).
- T2 hält eine Sperre auf Zeile mit `id = 2` und will `id = 1` ändern (blockiert durch T1).
- **Deadlock!**  
  PostgreSQL erkennt den Deadlock automatisch und **bricht eine der Transaktionen ab**, in diesem Fall T2.

**Ergebnis:**
- T2 wird durch die Datenbank **automatisch abgebrochen** (`ROLLBACK`), um den Deadlock aufzulösen.
- T1 kann anschließend **erfolgreich committen**.

**Fazit:**  
Ein Deadlock entsteht, wenn zwei (oder mehr) Transaktionen sich gegenseitig blockieren, ohne dass eine weiterkommen kann.  
PostgreSQL erkennt diesen Zustand und **erzwingt einen Rollback bei einer der Transaktionen**, um das System konsistent und funktionsfähig zu halten.





