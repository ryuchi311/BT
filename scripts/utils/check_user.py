
import os
from app import create_app
from models import db, User, DailyCheckIn

app = create_app()
with app.app_context():
    print(f"Checking for User with ID 1...")
    user = User.query.get(1)
    if user:
        print(f"User 1 exists: {user.username} (ID: {user.id})")
    else:
        print("User 1 does NOT exist.")

    print("\nChecking all users:")
    users = User.query.all()
    for u in users:
        print(f"User: {u.username}, ID: {u.id}")
