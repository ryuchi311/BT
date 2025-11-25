from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import db, User
from datetime import datetime

onboarding_bp = Blueprint('onboarding', __name__)

@onboarding_bp.route('/')
def show_onboarding():
    """Show onboarding page for new users"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))
    
    user = User.query.get(user_id)
    if user and user.is_onboarded:
        # Already onboarded, redirect to quests
        return redirect(url_for('quests.list_quests'))
    
    return render_template('onboarding.html', user=user)

@onboarding_bp.route('/complete', methods=['POST'])
def complete_onboarding():
    """Complete onboarding process"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    email = data.get('email')
    last_name = data.get('last_name', '').strip()
    terms_accepted = data.get('terms_accepted', False)
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    if not terms_accepted:
        return jsonify({'error': 'You must accept the terms and conditions'}), 400
    
    # Validate email format
    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Update user
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.email = email
    if last_name:
        user.last_name = last_name
    user.is_onboarded = True
    user.terms_accepted = True
    user.terms_accepted_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Onboarding completed successfully'
    })
