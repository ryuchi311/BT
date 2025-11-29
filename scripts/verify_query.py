import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models import Quest

if __name__ == '__main__':
    with app.app_context():
        try:
            q = Quest.query.limit(1).all()
            print('Query OK, fetched', len(q), 'rows')
        except Exception as e:
            print('Query failed:', repr(e))
