
from app import create_app
from models import db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    
    for table in ['user_quest', 'user_reward']:
        print(f"Checking {table}...")
        fks = inspector.get_foreign_keys(table)
        for fk in fks:
            print(f"  FK: {fk['name']} -> {fk['referred_table']}.{fk['referred_columns']}")
