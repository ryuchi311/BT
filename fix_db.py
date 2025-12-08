
from app import create_app
from models import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    conn = db.engine.connect()
    
    print("Dropping foreign key constraint 'daily_check_in_user_id_fkey'...")
    try:
        conn.execute(text("ALTER TABLE daily_check_in DROP CONSTRAINT daily_check_in_user_id_fkey"))
        print("Dropped.")
    except Exception as e:
        print(f"Error dropping constraint: {e}")
        # It might be that the constraint name varies if it was auto-generated differently, but previous inspection confirmed the name.

    print("Adding correct foreign key constraint...")
    try:
        # We need to make sure we point to "user" (singular)
        conn.execute(text("ALTER TABLE daily_check_in ADD CONSTRAINT daily_check_in_user_id_fkey FOREIGN KEY (user_id) REFERENCES \"user\" (id)"))
        print("Added new constraint referencing 'user'.")
        conn.commit()
    except Exception as e:
        print(f"Error adding constraint: {e}")
        conn.rollback()

    print("Done.")
