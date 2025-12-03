"""List tables in the target Postgres DB (Supabase) and optionally show row counts.
Usage:
  python scripts/list_tables.py       # list tables
  python scripts/list_tables.py --counts  # list tables with row counts
"""
import os
import sys
import argparse
from sqlalchemy import create_engine, text

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
except Exception:
    pass

parser = argparse.ArgumentParser()
parser.add_argument('--counts', action='store_true', help='Show approximate row counts')
args = parser.parse_args()

DB_URL = os.environ.get('DATABASE_URL') or os.environ.get('SUPABASE_DB_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')
if not DB_URL:
    print('ERROR: No DATABASE_URL/SUPABASE_DB_URL/SQLALCHEMY_DATABASE_URI found in environment or .env')
    sys.exit(1)

print('Connecting to:', DB_URL if len(DB_URL) < 160 else DB_URL[:160] + '...')

try:
    engine = create_engine(DB_URL, connect_args={'sslmode': 'require'} if DB_URL.startswith('postgres') else {}, future=True)
    with engine.connect() as conn:
        tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"))
        rows = [r[0] for r in tables]
        if not rows:
            print('No tables found in public schema.')
            sys.exit(0)
        print(f'Found {len(rows)} tables:')
        for t in rows:
            if args.counts:
                try:
                    c = conn.execute(text(f'SELECT COUNT(*) FROM "{t}"')).scalar()
                except Exception:
                    c = 'N/A'
                print(f' - {t} ({c} rows)')
            else:
                print(f' - {t}')
except Exception as e:
    print('Failed to list tables:', e)
    sys.exit(1)
