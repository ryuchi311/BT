"""Migrate data from local SQLite (instance/app.db) to target Postgres (Supabase).

Usage:
    & .\.venv\Scripts\Activate.ps1
    python scripts/migrate_to_supabase.py --source instance/app.db --target "$env:DATABASE_URL"

By default it reads DATABASE_URL or SUPABASE_DB_URL from environment.
This script is best-effort for small datasets and assumes target DB is empty or compatible.
"""
import os
import argparse
import json
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import URL

# Ensure project imports are available
import dotenv
dotenv.load_dotenv()

# Import app factory and models
from app import create_app
from config import Config
from models import db, User, Quest, Reward, UserQuest, DailyCheckIn, UserReward


def load_rows(engine, table_name):
    with engine.connect() as conn:
        res = conn.execute(text(f"SELECT * FROM \"{table_name}\"")).mappings().all()
        return [dict(r) for r in res]


def safe_load_json(value):
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except Exception:
        return value


def copy_table_rows(rows, Model, session, transform=None):
    created = 0
    for r in rows:
        data = dict(r)
        # transform platform/proof JSON fields
        if 'platform_config' in data:
            data['platform_config'] = safe_load_json(data.get('platform_config'))
        if 'proof_data' in data:
            data['proof_data'] = safe_load_json(data.get('proof_data'))
        # Some columns may not match exactly with model args; filter by model columns
        obj_kwargs = {}
        for col in data:
            # keep columns that exist on model
            if hasattr(Model, col):
                obj_kwargs[col] = data[col]
            else:
                # allow setting id explicitly even if not attribute on class (SQLAlchemy creates attribute)
                obj_kwargs[col] = data[col]
        # Truncate overly long string values to avoid target DB varchar limits
        for k, v in list(obj_kwargs.items()):
            try:
                if isinstance(v, str) and len(v) > 250:
                    obj_kwargs[k] = v[:247] + '...'
            except Exception:
                pass

        try:
            obj = Model(**obj_kwargs)
            session.add(obj)
            session.flush()
            created += 1
        except IntegrityError as e:
            session.rollback()
            print(f"IntegrityError inserting into {Model.__name__}: {e}")
        except TypeError:
            # fallback: set attributes manually
            try:
                obj = Model()
                for k, v in obj_kwargs.items():
                    try:
                        setattr(obj, k, v)
                    except Exception:
                        pass
                session.add(obj)
                session.flush()
                created += 1
            except Exception as e:
                session.rollback()
                print(f"Failed to add row to {Model.__name__}: {e}")
    return created


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='instance/app.db', help='Path to source SQLite DB (default: instance/app.db)')
    parser.add_argument('--target', default=None, help='Target DATABASE_URL (Postgres). If omitted, reads env DATABASE_URL or SUPABASE_DB_URL')
    parser.add_argument('--dry-run', action='store_true', help='Do not write to target DB; only report counts')
    args = parser.parse_args()

    src_path = args.source
    if not os.path.isabs(src_path):
        src_path = os.path.join(os.getcwd(), src_path)

    if not os.path.exists(src_path):
        print(f"Source DB not found: {src_path}")
        return

    target_url = args.target or os.environ.get('DATABASE_URL') or os.environ.get('SUPABASE_DB_URL')
    if not target_url:
        print("No target DATABASE_URL provided. Set DATABASE_URL or SUPABASE_DB_URL in environment or pass --target.")
        return

    sqlite_url = f"sqlite:///{src_path}"
    print(f"Source: {sqlite_url}")
    print(f"Target: {target_url}")

    # Create source engine
    src_engine = create_engine(sqlite_url, future=True)

    # Prepare target app with target DB by setting env before creating app
    os.environ['DATABASE_URL'] = target_url
    app = create_app()

    if args.dry_run:
        print("Dry run: will not write to target DB. Listing row counts...")
    with app.app_context():
        # create tables in target if not present
        if not args.dry_run:
            print('Ensuring target schema exists (create_all)...')
            db.create_all()

        # Load rows from source in order
        tables = [
            ('user', User),
            ('quest', Quest),
            ('reward', Reward),
            ('daily_check_in', DailyCheckIn),
            ('user_quest', UserQuest),
            ('user_reward', UserReward),
        ]

        summary = {}
        for table_name, Model in tables:
            try:
                rows = load_rows(src_engine, table_name)
            except Exception as e:
                # Try snake-case variants
                alt_name = table_name
                try:
                    rows = load_rows(src_engine, alt_name)
                except Exception as e2:
                    print(f"Could not read table {table_name}: {e} / {e2}")
                    rows = []

            print(f"Found {len(rows)} rows in source table {table_name}")
            summary[table_name] = len(rows)
            if args.dry_run:
                continue

            created = copy_table_rows(rows, Model, db.session)
            db.session.commit()
            print(f"Inserted {created} rows into {Model.__name__}")

        print('\nMigration summary:')
        for k, v in summary.items():
            print(f" - {k}: {v} rows")

    print('Done.')


if __name__ == '__main__':
    main()
