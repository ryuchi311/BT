"""Create any missing tables (runs `db.create_all()` in app context).

Usage:
  & .\.venv\Scripts\Activate.ps1
  python scripts/create_missing_tables.py
"""
import os
import sys
sys.path.insert(0, os.getcwd())

from app import create_app
from models import db, AdminUser

app = create_app()
with app.app_context():
    print('Creating missing tables (db.create_all())...')
    db.create_all()
    try:
        count = AdminUser.query.count()
    except Exception as e:
        print('AdminUser query failed:', e)
        count = 'unknown'
    print('AdminUser count:', count)
print('Done.')
