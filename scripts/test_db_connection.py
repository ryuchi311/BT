"""Quick DB connectivity tester.
Reads `DATABASE_URL` or `SUPABASE_DB_URL` from .env (via python-dotenv) and attempts a simple SELECT 1.
Exit code 0 on success, 1 on failure.
"""
import os
import sys
import traceback
from sqlalchemy import create_engine, text

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

if load_dotenv:
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

db_url = os.environ.get('DATABASE_URL') or os.environ.get('SUPABASE_DB_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')
if not db_url:
    print('ERROR: No DATABASE_URL/SUPABASE_DB_URL/SQLALCHEMY_DATABASE_URI found in environment or .env')
    sys.exit(1)

print('Using DB URL:', db_url if len(db_url) < 200 else db_url[:200] + '...')

# Try to connect
try:
    # If it's a Postgres URL, ensure sslmode when using Supabase
    connect_args = {}
    if db_url.startswith('postgres') or 'supabase' in db_url:
        connect_args = {'sslmode': 'require'}

    engine = create_engine(db_url, connect_args=connect_args, future=True)
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        val = result.scalar()
        print('SELECT 1 ->', val)
        # show PG version if possible
        try:
            ver = conn.execute(text('SELECT version()')).scalar()
            print('Server version:', ver)
        except Exception:
            pass
    print('Connection test succeeded.')
    sys.exit(0)
except Exception as exc:
    print('Connection test failed:')
    traceback.print_exc()
    sys.exit(1)
