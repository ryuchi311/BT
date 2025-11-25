from app import app, db
from models import User, Quest, SystemSetting

with app.app_context():
    db.create_all()
    
    # Create a test user if not exists
    if not User.query.filter_by(username='Traveler').first():
        user = User(telegram_id='12345', username='Traveler', points=100, xp=50)
        db.session.add(user)
        
    # Create some sample quests with new fields
    if not Quest.query.first():
        quests = [
            Quest(
                title='Join Telegram Group', 
                description='Join our official group and stay updated with the latest news',
                points=50, 
                quest_type='telegram', 
                action_url='https://t.me/example',
                category='Social',
                verification_data='@examplechannel'
            ),
            Quest(
                title='Follow on Twitter', 
                description='Follow us for updates and announcements',
                points=30, 
                quest_type='twitter', 
                action_url='https://twitter.com/example',
                category='Social'
            ),
            Quest(
                title='Watch YouTube Video', 
                description='Learn about the project by watching our introduction video',
                points=20, 
                quest_type='youtube', 
                action_url='https://youtube.com/example',
                category='Educational'
            ),
            Quest(
                title='Visit Website', 
                description='Check out our roadmap and learn about upcoming features',
                points=10, 
                quest_type='visit', 
                action_url='https://example.com',
                category='Engagement'
            )
        ]
        db.session.add_all(quests)
        
    db.session.commit()
    print("Database initialized with sample data!")
