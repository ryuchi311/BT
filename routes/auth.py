from flask import Blueprint, request, jsonify, session, redirect, url_for
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/telegram', methods=['POST'])
def telegram_auth():
    data = request.get_json(silent=True) or {}

    telegram_id = data.get('id') or data.get('telegram_id')
    if not telegram_id:
        return jsonify({'status': 'error', 'error': 'Missing telegram id'}), 400

    telegram_id = str(telegram_id)
    user = User.query.filter_by(telegram_id=telegram_id).first()

    if not user:
        user = User(telegram_id=telegram_id)
        db.session.add(user)

    # Update mutable profile fields from Telegram payload
    user.username = data.get('username') or user.username
    user.first_name = data.get('first_name') or user.first_name
    user.last_name = data.get('last_name') or user.last_name
    user.photo_url = data.get('photo_url') or user.photo_url

    db.session.commit()

    session['user_id'] = user.id
    session.permanent = True

    next_step = 'home'
    if not user.is_onboarded or not user.email:
        next_step = 'onboarding'

    return jsonify({
        'status': 'success',
        'user': user.to_dict(),
        'next': next_step
    })

@auth_bp.route('/dev_login/<int:user_id>')
def dev_login(user_id):
    # Backdoor for local dev
    session['user_id'] = user_id
    session.permanent = True
    return redirect(url_for('main.index'))
