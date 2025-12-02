import sqlite3, json, sys

db = 'instance/app.db'
try:
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("PRAGMA table_info('user')")
    cols = [{'cid': r[0], 'name': r[1], 'type': r[2], 'notnull': r[3], 'dflt_value': r[4], 'pk': r[5]} for r in c.fetchall()]
    print(json.dumps(cols, indent=2))
except Exception as e:
    print('ERROR', e)
    sys.exit(1)
finally:
    try:
        conn.close()
    except Exception:
        pass
