from flask import Blueprint, render_template, session, redirect, url_for
from models import User, Quest, UserQuest, db
from flask import g

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Mock user for dev if not authenticated
    user = getattr(g, 'user', None)
    if not user:
        # For prototype, just show a demo user or redirect to auth
        # We'll pass a dummy user object for the template to render
        user = {'username': 'Traveler', 'points': 0, 'xp': 0}
    
    return render_template('index.html', user=user)

@main_bp.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.points.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users)

@main_bp.route('/test-login')
def test_login():
    """Quick test login for development - creates/uses a test user"""
    # Check if test user exists
    test_user = User.query.filter_by(telegram_id='test_user_123').first()
    
    if not test_user:
        # Create test user
        test_user = User(
            telegram_id='test_user_123',
            username='TestUser',
            first_name='Test',
            points=100,
            xp=100
        )
        db.session.add(test_user)
        db.session.commit()
    
    # Set session
    session['user_id'] = test_user.id
    session['telegram_id'] = test_user.telegram_id
    
    return redirect(url_for('quests.list_quests'))
