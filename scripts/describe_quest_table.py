import sqlite3, json

dbs = ['app.db', 'instance/app.db']
for p in dbs:
    print('\nDB:', p)
    try:
        conn = sqlite3.connect(p)
        cur = conn.cursor()
        rows = cur.execute("PRAGMA table_info('quest')").fetchall()
        # print as list of dicts for readability
        cols = []
        for r in rows:
            cols.append({
                'cid': r[0], 'name': r[1], 'type': r[2], 'notnull': r[3], 'dflt_value': r[4], 'pk': r[5]
            })
        print(json.dumps(cols, indent=2))
        conn.close()
    except Exception as e:
        print('ERROR:', e)
