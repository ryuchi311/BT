
from app import create_app
from models import db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tables:", tables)
    
    # Check foreign keys for daily_check_in
    if 'daily_check_in' in tables:
        fks = inspector.get_foreign_keys('daily_check_in')
        for fk in fks:
            print(f"FK: {fk}")
