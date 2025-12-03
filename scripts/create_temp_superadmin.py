"""Create a temporary superadmin username/password in SystemSetting.

Usage:
  & .\.venv\Scripts\Activate.ps1
  python scripts/create_temp_superadmin.py

Prints the created credentials to stdout. If credentials already exist it will print them (password is not recoverable; it will generate a new one if --force).
"""
import os
import secrets
import dotenv
from werkzeug.security import generate_password_hash

dotenv.load_dotenv()

# Ensure app imports resolve
import sys
sys.path.insert(0, os.getcwd())

from app import create_app
from models import db, SystemSetting, AdminUser


def _get_setting(key):
    return SystemSetting.query.get(key)


def _set_setting(key, value):
    s = SystemSetting.query.get(key)
    if not s:
        s = SystemSetting(key=key, value=value)
        db.session.add(s)
    else:
        s.value = value
    db.session.commit()


def main():
    app = create_app()
    with app.app_context():
        existing_user = _get_setting('superadmin.username')
        existing_hash = _get_setting('superadmin.password_hash')
        if existing_user and existing_hash:
            print('Superadmin username already set in DB (stored in SystemSetting).')
            print('Username:', existing_user.value)
            print('If you want to overwrite, re-run with --force (not implemented interactively).')
            return

        username = 'superadmin'
        password = secrets.token_urlsafe(10)
        pw_hash = generate_password_hash(password)
        _set_setting('superadmin.username', username)
        _set_setting('superadmin.password_hash', pw_hash)
        # Also create an AdminUser row for management UI if missing
        if not AdminUser.query.filter_by(username=username).first():
            admin = AdminUser(username=username, password_hash=pw_hash, is_superadmin=True)
            db.session.add(admin)
            db.session.commit()
        print('Temporary superadmin credentials created:')
        print('  username:', username)
        print('  password:', password)
        print('\nStore these credentials securely. They are intended as temporary admin access.')


if __name__ == '__main__':
    main()
