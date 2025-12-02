import sqlite3

db = 'instance/app.db'
print('Using DB:', db)
conn = sqlite3.connect(db)
cur = conn.cursor()
cols = cur.execute("PRAGMA table_info('quest')").fetchall()
col_names = [c[1] for c in cols]
print('Existing columns:', col_names)
if 'starts_at' in col_names:
    print('Column `starts_at` already exists. No action taken.')
else:
    print('Adding `starts_at` column...')
    try:
        cur.execute("ALTER TABLE quest ADD COLUMN starts_at TIMESTAMP NULL")
        conn.commit()
        print('Column added successfully.')
    except Exception as e:
        print('Failed to add column:', e)
conn.close()
