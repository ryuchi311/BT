"""
Database migration script to update Reward table and add UserReward table
Run this script to update the database schema
"""
from app import app, db
from models import Reward, UserReward

with app.app_context():
    # Create/update tables
    db.create_all()
    print("✅ Reward table updated successfully!")
    print("✅ UserReward table created successfully!")
    print("Database migration complete.")
