from flask import Blueprint, render_template, request, jsonify, session
from models import db, User, UserQuest
from functools import wraps

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

    return render_template('profile.html', user=user)

@profile_bp.route('/')
@login_required
def view_profile():
    """Display user profile page"""
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'status': 'error', 'error': 'User not found'}), 404
        
    # Fetch User Activity
    # We want recently submitted/updated quests
    activities = user.quests.order_by(db.desc('submitted_at')).limit(20).all()
    
    # Calculate detailed stats
    stats = {
        'approved': user.quests.filter_by(status='approved').count(),
        'pending': user.quests.filter(UserQuest.status.in_(['pending', 'submitted'])).count(),
        'rejected': user.quests.filter_by(status='rejected').count()
    }
    
    return render_template('profile.html', user=user, activities=activities, stats=stats)

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
            
        # Update social fields
        social_fields = ['twitter_handle', 'discord_id', 'facebook_profile', 'instagram_profile', 'youtube_handle']
        for field in social_fields:
            if field in data:
                setattr(user, field, data[field].strip() if data[field] and data[field].strip() else None)
        
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
