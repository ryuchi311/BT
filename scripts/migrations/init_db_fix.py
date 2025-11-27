from app import app
from models import db, User, Quest, Reward

with app.app_context():
    db.create_all()
    print('Created tables')

    # Create a simple test user if none exist
    if not User.query.filter_by(username='Traveler').first():
        user = User(telegram_id='12345', username='Traveler', points=100, xp=50)
        db.session.add(user)

    if not Quest.query.first():
        q = Quest(title='Sample Quest', description='Setup done', quest_type='visit', points=10)
        db.session.add(q)

    if not Reward.query.first():
        r = Reward(title='Sample Reward', description='Welcome reward', cost=10)
        db.session.add(r)

    db.session.commit()
    print('Database initialized (fix script)')
