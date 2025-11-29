import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models import db
from sqlalchemy import text

sql = """
ALTER TABLE quest
ADD COLUMN IF NOT EXISTS starts_at TIMESTAMP;
"""

if __name__ == '__main__':
    with app.app_context():
        print('Executing SQL to add starts_at column...')
        try:
            with db.engine.begin() as conn:
                conn.execute(text(sql))
            print('ALTER TABLE executed successfully.')
        except Exception as e:
            print('Error executing ALTER TABLE:', repr(e))
