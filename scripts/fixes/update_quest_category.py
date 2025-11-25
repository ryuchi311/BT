"""
Script to change Daily Check-in quest category from Engagement to Social
"""
from app import app, db
from models import Quest

with app.app_context():
    # Find the Daily Check-in quest
    daily_checkin = Quest.query.filter_by(title='Daily Check-in').first()
    
    if daily_checkin:
        print(f"\nFound quest: {daily_checkin.title}")
        print(f"Current category: {daily_checkin.category}")
        
        # Change category to Social
        daily_checkin.category = 'Social'
        db.session.commit()
        
        print(f"✅ Updated category to: {daily_checkin.category}")
        print("\nQuest updated successfully!")
    else:
        print("❌ Daily Check-in quest not found")
    
    # Show all quests with their categories
    print("\n=== All Quest Categories ===\n")
    quests = Quest.query.all()
    for quest in quests:
        print(f"{quest.title}: {quest.category}")
