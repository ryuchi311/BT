
from app import create_app
from models import db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tables:", tables)
    
    if 'daily_check_in' in tables:
        fks = inspector.get_foreign_keys('daily_check_in')
        for fk in fks:
            print(f"FK Name: {fk['name']}")
            print(f"Constrained Cols: {fk['constrained_columns']}")
            print(f"Referred Table: {fk['referred_table']}")
            print(f"Referred Cols: {fk['referred_columns']}")
            print("-" * 20)

    # Check users table content again
    conn = db.engine.connect()
    # Check if 'user' table exists
    if 'user' in tables:
        print("Table 'user' exists.")
    else:
        print("Table 'user' does NOT exist.")

    if 'users' in tables:
        print("Table 'users' exists.")
        from sqlalchemy import text
        result = conn.execute(text("SELECT id FROM users WHERE id = 1"))
        row = result.first()
        if row:
            print("Row with id=1 FOUND in 'users'.")
        else:
            print("Row with id=1 NOT FOUND in 'users'.")
    
