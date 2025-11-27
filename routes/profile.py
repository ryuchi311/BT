from flask import Blueprint, render_template, request, jsonify, session
from models import db, User, UserQuest, DailyCheckIn, UserReward
from functools import wraps
from datetime import datetime

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@profile_bp.route('/')
@login_required
def view_profile():
    """Display user profile page"""
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'status': 'error', 'error': 'User not found'}), 404
    
    # Fetch completed quests
    completed_quests = UserQuest.query.filter_by(user_id=user.id, status='completed').all()
    
    # Fetch check-ins
    checkins = DailyCheckIn.query.filter_by(user_id=user.id).all()
    
    # Fetch rewards
    rewards = UserReward.query.filter_by(user_id=user.id).all()
    
    activities = []
    
    for uq in completed_quests:
        activities.append({
            'type': 'quest',
            'title': uq.quest.title,
            'date': uq.completed_at or uq.submitted_at or datetime.min,
            'points': uq.quest.points,
            'icon': 'fa-scroll'
        })
        
    for ci in checkins:
        # Convert date to datetime for sorting
        dt = datetime.combine(ci.check_in_date, datetime.min.time())
        activities.append({
            'type': 'checkin',
            'title': f"Daily Check-in: {ci.quest.title}",
            'date': dt,
            'points': ci.quest.points,
            'icon': 'fa-calendar-check'
        })
        
    for ur in rewards:
        activities.append({
            'type': 'reward',
            'title': f"Claimed: {ur.reward.title}",
            'date': ur.claimed_at,
            'points': -ur.reward.cost,
            'icon': 'fa-gift'
        })
        
    # Sort by date desc
    activities.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('profile.html', user=user, activities=activities)

@profile_bp.route('/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'status': 'error', 'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update email if provided
        if 'email' in data and data['email']:
            user.email = data['email']
        
        # Update last name if provided
        if 'last_name' in data:
            user.last_name = data['last_name'] if data['last_name'] else None
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Profile updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
