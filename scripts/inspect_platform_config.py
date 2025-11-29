import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models import Quest

if __name__ == '__main__':
    with app.app_context():
        qs = Quest.query.order_by(Quest.id.desc()).limit(50).all()
        for q in qs:
            print(f'ID={q.id} TITLE="{q.title}" PLATFORM_CONFIG={q.platform_config}')
