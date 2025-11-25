"""
Script to check quest categories in the database
"""
from app import app, db
from models import Quest

with app.app_context():
    quests = Quest.query.all()
    print("\n=== Quest Categories ===\n")
    for quest in quests:
        print(f"ID: {quest.id}")
        print(f"Title: {quest.title}")
        print(f"Type: {quest.quest_type}")
        print(f"Category: {quest.category}")
        print("-" * 40)
