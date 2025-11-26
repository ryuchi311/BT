from flask import Blueprint, render_template, request, jsonify, session
from models import db, User
from functools import wraps

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
    
    return render_template('profile.html', user=user)

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
