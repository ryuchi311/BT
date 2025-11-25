from app import app, db
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    print("Tables in database:")
    for table_name in inspector.get_table_names():
        print(f"- {table_name}")
