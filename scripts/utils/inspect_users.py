
from app import create_app
from models import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    conn = db.engine.connect()
    
    print("Content of 'user' table (ID 1):")
    res_user = conn.execute(text("SELECT * FROM \"user\" WHERE id = 1")).fetchone()
    print(res_user)

    print("\nContent of 'users' table (All):")
    res_users = conn.execute(text("SELECT * FROM users")).fetchall()
    print(res_users)
