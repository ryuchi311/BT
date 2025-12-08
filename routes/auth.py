from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
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
            photo_url=data.get('photo_url'),
            is_onboarded=True # Telegram users are auto-onboarded for now or redirect to profile
        )
        db.session.add(user)
        db.session.commit()
    
    session['user_id'] = user.id
    return jsonify({'status': 'success', 'user': user.to_dict()})

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('user_id'):
            return redirect(url_for('main.index'))
        return render_template('login.html')
    
    # Handle Email Login (Passwordless)
    email = request.form.get('email')
    if not email:
        # Should show error
        return render_template('login.html', error="Email is required")
    
    email = email.lower().strip()
    
    user = User.query.filter_by(email=email).first()
    if not user:
        # Create new user
        # We need a unique placeholder telegram_id since it's nullable=False and unique
        # For email users, we can generate a unique ID or make telegram_id nullable (better).
        # But for now, let's look at models.py. telegram_id is NOT NULL.
        # We must generate one or change the model.
        # Generating a fake one based on email is easiest for now without DB migration.
        import uuid
        from datetime import datetime
        fake_tg_id = f"email_{uuid.uuid4().hex[:16]}"
        
        user = User(
            email=email,
            telegram_id=fake_tg_id,
            username=email.split('@')[0],
            is_onboarded=True, # Email users are auto-onboarded
            terms_accepted=True,
            terms_accepted_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        
    session['user_id'] = user.id
    return redirect(url_for('main.index'))

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/dev_login/<int:user_id>')
def dev_login(user_id):
    # Backdoor for local dev
    session['user_id'] = user_id
    return redirect(url_for('main.index'))
