"""
Schema sync helper
- Loads SQLAlchemy model classes from `models.py`
- Compares each model's table columns to the SQLite file (default `instance/app.db`)
- Adds any missing columns via `ALTER TABLE ... ADD COLUMN` using a best-effort type mapping

Usage:
  # quick run with default DB
  python scripts/schema_sync.py

  # override DB via env var (SQLALCHEMY_DATABASE_URI)
  setx SQLALCHEMY_DATABASE_URI "sqlite:///instance/app.db"
  $env:SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/app.db'
  python scripts/schema_sync.py

Caveats:
- Adds columns as NULLABLE only (no NOT NULL constraints are applied)
- Attempts to use the SQLAlchemy column type string (e.g. VARCHAR(128), INTEGER)
- Does not attempt to migrate or copy data for renamed/dropped columns
"""

import os
import sqlite3
import inspect
import models


def _db_path_from_uri(uri: str):
    if not uri:
        return 'instance/app.db'
    uri = uri.strip()
    if uri.startswith('sqlite:///'):
        return uri.replace('sqlite:///', '')
    if uri.startswith('sqlite:'):
        # fallback to last part
        return uri.split(':', 1)[-1]
    # assume it's a file path
    return uri


def sql_type_from_col(col):
    # Best-effort: use the string form of the SQLAlchemy type
    t = str(col.type)
    t = t.upper()
    # Normalize JSON/BOOLEAN types for SQLite where supported
    if 'JSON' in t:
        return 'JSON'
    if 'BOOLEAN' in t:
        return 'BOOLEAN'
    if 'INTEGER' in t or 'INT' in t:
        return 'INTEGER'
    if 'TIMESTAMP' in t or 'DATETIME' in t:
        return 'TIMESTAMP'
    if 'TEXT' in t:
        return 'TEXT'
    if 'CHAR' in t or 'VARCHAR' in t or 'STRING' in t:
        return t
    if 'FLOAT' in t or 'NUMERIC' in t or 'DECIMAL' in t:
        return 'REAL'
    # fallback
    return t


def find_model_classes(mod):
    for name in dir(mod):
        if name.startswith('_'):
            continue
        obj = getattr(mod, name)
        if inspect.isclass(obj) and hasattr(obj, '__table__'):
            yield obj


def main():
    uri = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///instance/app.db'
    db_path = _db_path_from_uri(uri)
    print(f'Using DB path: {db_path}')

    if not os.path.exists(db_path):
        print('Database file not found:', db_path)
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    models_to_check = list(find_model_classes(models))
    if not models_to_check:
        print('No model classes with __table__ found in models.py')
        conn.close()
        return

    for model in models_to_check:
        table = model.__table__.name
        print(f'\nChecking table: {table}')
        try:
            existing = [r[1] for r in cur.execute(f"PRAGMA table_info('{table}')").fetchall()]
        except Exception as e:
            print('  Table does not exist in DB:', table)
            continue

        missing = []
        for col in model.__table__.columns:
            if col.name not in existing:
                missing.append(col)

        if not missing:
            print('  No missing columns')
            continue

        print('  Missing columns:', [c.name for c in missing])
        for col in missing:
            sql_type = sql_type_from_col(col)
            # Add column as nullable; avoid default/NOT NULL complexity
            alter_sql = f"ALTER TABLE {table} ADD COLUMN {col.name} {sql_type} NULL"
            print('   ->', alter_sql)
            try:
                cur.execute(alter_sql)
                conn.commit()
                print('      Added')
            except Exception as e:
                print('      Failed to add column', col.name, '->', e)

    conn.close()
    print('\nDone.')


if __name__ == '__main__':
    main()
