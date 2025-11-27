import os
import sys

# Ensure project root is on sys.path so imports like `import app` work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db

with app.app_context():
    db.create_all()
    print('DB created (init_db_run)')
