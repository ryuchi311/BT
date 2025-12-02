import sqlite3, json, sys

db = 'app.db'
try:
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [r[0] for r in c.fetchall()]
    print(json.dumps(tables, indent=2))
except Exception as e:
    print('ERROR', e)
    sys.exit(1)
finally:
    try:
        conn.close()
    except Exception:
        pass
