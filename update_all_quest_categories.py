"""
Script to check and update quest categories
"""
from app import app, db
from models import Quest

with app.app_context():
    quests = Quest.query.all()
    
    print("\n=== Current Quest Categories ===\n")
    for quest in quests:
        print(f"ID: {quest.id}, Title: {quest.title}, Category: {quest.category or 'NONE'}")
    
    # Update quests without categories
    print("\n=== Updating quests without categories ===\n")
    
    for quest in quests:
        if not quest.category:
            # Assign default category based on quest type
            if quest.quest_type in ['telegram', 'twitter']:
                quest.category = 'Social'
            elif quest.quest_type == 'youtube':
                quest.category = 'Educational'
            elif quest.quest_type in ['daily_checkin', 'visit']:
                quest.category = 'Engagement'
            else:
                quest.category = 'Social'
            
            print(f"✅ Updated {quest.title}: {quest.category}")
    
    db.session.commit()
    
    print("\n=== Final Quest Categories ===\n")
    quests = Quest.query.all()
    for quest in quests:
        print(f"ID: {quest.id}, Title: {quest.title}, Category: {quest.category}")
