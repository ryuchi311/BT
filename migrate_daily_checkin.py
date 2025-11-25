"""
Database migration script to add DailyCheckIn table
Run this script to update the database schema
"""
from app import app, db
from models import DailyCheckIn

with app.app_context():
    # Create the DailyCheckIn table
    db.create_all()
    print("✅ DailyCheckIn table created successfully!")
    print("Database migration complete.")
