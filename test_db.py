import os, psycopg2, urllib.parse, traceback
url = os.environ.get("DATABASE_URL")
if not url:
    print("NO_DATABASE_URL")
    raise SystemExit(1)
p = urllib.parse.urlparse(url)
host = p.hostname
port = p.port or 5432
print(f"ATTEMPT_DB_CONNECT host={host} port={port}")
try:
    conn = psycopg2.connect(dsn=url, connect_timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print("DB_OK", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("DB_CONNECT_FAIL", repr(e))
    traceback.print_exc()
