from flask import Blueprint, request, jsonify, session, redirect, url_for
from models import db, User
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/telegram', methods=['POST'])
def telegram_auth():
    data = request.json
    # Verify telegram data hash here (omitted for prototype simplicity)
    
    telegram_id = str(data.get('id'))
    user = User.query.filter_by(telegram_id=telegram_id).first()
    
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=data.get('username'),
            first_name=data.get('first_name'),
            photo_url=data.get('photo_url')
        )
        db.session.add(user)
        db.session.commit()
    
    session['user_id'] = user.id
    return jsonify({'status': 'success', 'user': user.to_dict()})

@auth_bp.route('/dev_login/<int:user_id>')
def dev_login(user_id):
    # Backdoor for local dev
    session['user_id'] = user_id
    return redirect(url_for('main.index'))
