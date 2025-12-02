"""
Small migration helper to add missing columns to the `user` table in SQLite.

Usage (from repo root):
    python scripts/migrate_add_user_columns.py

This script uses SQLAlchemy to read the current table schema and issues
`ALTER TABLE ... ADD COLUMN` for any columns that exist in `models.User` but
are missing in the database. Columns are added as NULLABLE to be safe.

Note: keep a backup of your DB before running in production.
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.engine import reflection

# Try to load DB URL from config or environment
DB_URL = None
try:
    # Prefer environment variable
    DB_URL = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')
except Exception:
    DB_URL = None

if not DB_URL:
    # Fallback to config.py if present
    try:
        # When running this file directly python sets sys.path[0] to the scripts/ directory.
        # Ensure project root is on sys.path so `import config` works.
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        from config import Config
        DB_URL = getattr(Config, 'SQLALCHEMY_DATABASE_URI', None) or getattr(Config, 'DATABASE_URL', None)
    except Exception as e:
        print('Importing config failed:', e)
        DB_URL = None

if not DB_URL:
    print('ERROR: Could not determine the database URL. Set DATABASE_URL or SQLALCHEMY_DATABASE_URI env var or configure config.Config.'); sys.exit(1)

print('Using DB URL:', DB_URL)
engine = create_engine(DB_URL, future=True)
inspector = reflection.Inspector.from_engine(engine)

expected_columns = {
    'telegram_id': 'TEXT',
    'username': 'TEXT',
    'first_name': 'TEXT',
    'last_name': 'TEXT',
    'photo_url': 'TEXT',
    'email': 'TEXT',
    'is_onboarded': 'BOOLEAN',
    'terms_accepted': 'BOOLEAN',
    'terms_accepted_at': 'DATETIME',
    'xp': 'INTEGER',
    'points': 'INTEGER',
    'created_at': 'DATETIME'
}

with engine.connect() as conn:
    tables = inspector.get_table_names()
    if 'user' not in tables:
        print('ERROR: No `user` table found in the database. Aborting.')
        sys.exit(1)

    existing = {col['name'] for col in inspector.get_columns('user')}
    to_add = []
    for colname, coltype in expected_columns.items():
        if colname not in existing:
            to_add.append((colname, coltype))

    if not to_add:
        print('No missing columns detected. Database schema already matches model (for user table).')
        sys.exit(0)

    print('Columns to add:', ', '.join(c for c, t in to_add))
    print('Adding columns as NULLABLE. This is safe for SQLite. (Backup DB first!)')

    for colname, coltype in to_add:
        # SQLite allows simple ALTER TABLE ADD COLUMN <name> <type>;
        stmt = text(f'ALTER TABLE "user" ADD COLUMN "{colname}" {coltype} NULL;')
        try:
            conn.execute(stmt)
            print(f'Added column {colname} ({coltype})')
        except Exception as e:
            print(f'Failed to add column {colname}:', e)

    # Ensure changes are persisted for SQLite
    try:
        conn.commit()
    except Exception:
        pass

print('Migration complete. Restart your application and verify the error is resolved.')
