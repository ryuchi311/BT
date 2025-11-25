from app import app, db
from models import User, Quest, Reward, SystemSetting

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
        
    # Create sample rewards
    if not Reward.query.first():
        rewards = [
            Reward(
                title='Amazon Gift Card $10',
                description='Digital code for Amazon US store',
                cost=500,
                image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/2560px-Amazon_logo.svg.png',
                stock=10,
                category='Voucher'
            ),
            Reward(
                title='Premium Sticker Pack',
                description='Exclusive Telegram sticker pack',
                cost=100,
                image_url='https://cdn-icons-png.flaticon.com/512/4712/4712109.png',
                stock=None, # Unlimited
                category='Digital'
            ),
            Reward(
                title='Discord Nitro 1 Month',
                description='Boost your Discord experience',
                cost=1000,
                image_url='https://assets-global.website-files.com/6257adef93867e56f84d3092/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png',
                stock=5,
                category='Voucher'
            )
        ]
        db.session.add_all(rewards)
        print("Added sample rewards")
        
    db.session.commit()
    print("Database initialized with sample data!")
