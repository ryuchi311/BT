from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from models import db, Quest, UserQuest, User, DailyCheckIn
from datetime import datetime, date, timedelta
import os
import requests

quests_bp = Blueprint('quests', __name__)

@quests_bp.route('/')
def list_quests():
    user_id = session.get('user_id')
    
    # Check if user needs onboarding
    if user_id:
        user = User.query.get(user_id)
        if user and not user.is_onboarded:
            return redirect(url_for('onboarding.show_onboarding'))
    
    quests = Quest.query.filter_by(is_active=True).order_by(Quest.id.desc()).all()
    
    # Get completed quests for this user
    completed_quest_ids = []
    user_quests = {}
    if user_id:
        completed = UserQuest.query.filter(
            UserQuest.user_id == user_id,
            UserQuest.status.in_(['completed', 'approved'])
        ).all()
        completed_quest_ids = [uq.quest_id for uq in completed]

        # Map latest submission per quest for quick lookups
        submissions = UserQuest.query.filter_by(user_id=user_id).order_by(UserQuest.id.desc()).all()
        for submission in submissions:
            if submission.quest_id not in user_quests:
                user_quests[submission.quest_id] = submission
    
    # Get check-in status for daily quests
    checkin_status = {}
    if user_id:
        today = date.today()
        for quest in quests:
            if quest.quest_type == 'daily_checkin':
                # Check if checked in today
                checkin = DailyCheckIn.query.filter_by(
                    user_id=user_id,
                    quest_id=quest.id,
                    check_in_date=today
                ).first()
                
                if checkin:
                    checkin_status[quest.id] = {
                        'checked_in': True,
                        'streak': checkin.streak_count
                    }
                else:
                    # Get last check-in for streak info
                    last_checkin = DailyCheckIn.query.filter_by(
                        user_id=user_id,
                        quest_id=quest.id
                    ).order_by(DailyCheckIn.check_in_date.desc()).first()
                    
                    checkin_status[quest.id] = {
                        'checked_in': False,
                        'streak': last_checkin.streak_count if last_checkin else 0
                    }
    
    return render_template(
        'quests.html',
        quests=quests,
        checkin_status=checkin_status,
        completed_quest_ids=completed_quest_ids,
        user_quests=user_quests
    )

@quests_bp.route('/verify/<int:quest_id>')
def verify_quest(quest_id):
    """Show verification page for YouTube quests"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))
    
    quest = Quest.query.get_or_404(quest_id)
    user = User.query.get(user_id)
    
    # Check if already completed
    existing = UserQuest.query.filter_by(
        user_id=user_id,
        quest_id=quest_id,
        status='completed'
    ).first()
    
    if existing:
        return redirect(url_for('quests.list_quests'))

    existing_submission = UserQuest.query.filter_by(
        user_id=user_id,
        quest_id=quest_id
    ).order_by(UserQuest.id.desc()).first()

    if existing_submission and existing_submission.status == 'completed':
        existing_submission = None
    
    return render_template('quest_verify.html', quest=quest, user=user, existing_submission=existing_submission)

@quests_bp.route('/verify-code/<int:quest_id>', methods=['POST'])
def verify_code(quest_id):
    """Verify the code entered by user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    code = data.get('code', '').strip()
    
    quest = Quest.query.get_or_404(quest_id)
    user = User.query.get(user_id)
    
    # Check if already completed
    existing = UserQuest.query.filter_by(
        user_id=user_id,
        quest_id=quest_id,
        status='completed'
    ).first()
    
    if existing:
        return jsonify({'success': False, 'error': 'Quest already completed'}), 400
    
    # Verify code
    if not quest.verification_code:
        return jsonify({'success': False, 'error': 'No verification code set for this quest'}), 400
    
    if code.upper() == quest.verification_code.upper():
        # Mark as completed and award points
        if not existing:
            uq = UserQuest(user_id=user_id, quest_id=quest_id, status='completed', completed_at=datetime.utcnow())
            db.session.add(uq)
        else:
            existing.status = 'completed'
            existing.completed_at = datetime.utcnow()
        
        user.points += quest.points
        user.xp += quest.points
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'points': quest.points,
            'new_total_points': user.points
        })
    else:
        return jsonify({'success': False, 'error': 'Invalid code. Please try again.'}), 400

@quests_bp.route('/complete/<int:quest_id>', methods=['POST'])
def complete_quest(quest_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    # Check if already completed
    existing = UserQuest.query.filter_by(user_id=user_id, quest_id=quest_id).order_by(UserQuest.id.desc()).first()
    if existing and existing.status == 'completed':
        return jsonify({'error': 'Already completed'}), 400
        
    quest = Quest.query.get_or_404(quest_id)
    if quest.quest_type == 'manual':
        return jsonify({'error': 'Manual quests require proof submission for review'}), 400
    user = User.query.get(user_id)
    
    # Here we would add specific verification logic based on quest.quest_type
    # For prototype, we assume instant completion
    
    if not existing:
        uq = UserQuest(user_id=user_id, quest_id=quest_id, status='completed', completed_at=datetime.utcnow())
        db.session.add(uq)
    else:
        existing.status = 'completed'
        existing.completed_at = datetime.utcnow()
        
    user.points += quest.points
    user.xp += quest.points # 1 point = 1 XP for now
    
    db.session.commit()
    
    return jsonify({'status': 'success', 'new_points': user.points})

@quests_bp.route('/manual-submit/<int:quest_id>', methods=['POST'])
def submit_manual_quest(quest_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    quest = Quest.query.get_or_404(quest_id)
    if quest.quest_type != 'manual':
        return jsonify({'error': 'Invalid quest type'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    proof_link = (request.form.get('proof_link') or '').strip()
    notes = (request.form.get('notes') or '').strip()

    if not proof_link:
        return jsonify({'error': 'Please provide a proof link so we can verify your submission.'}), 400

    existing = UserQuest.query.filter_by(user_id=user_id, quest_id=quest_id).first()

    if existing and existing.status == 'completed':
        return jsonify({'error': 'Quest already completed'}), 400

    if not existing:
        existing = UserQuest(user_id=user_id, quest_id=quest_id)
        db.session.add(existing)

    existing.status = 'submitted'
    existing.submission_link = proof_link or None
    existing.submission_text = notes or None
    existing.submitted_at = datetime.utcnow()
    existing.verification_status = 'pending'
    existing.completed_at = None
    existing.admin_notes = None
    existing.proof_data = None

    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Submission received! Our team will review your proof and award points once approved.'
    })

@quests_bp.route('/manual-ack/<int:quest_id>', methods=['POST'])
def acknowledge_manual_rejection(quest_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    quest = Quest.query.get_or_404(quest_id)
    if quest.quest_type != 'manual':
        return jsonify({'error': 'Invalid quest type'}), 400

    submission = UserQuest.query.filter_by(user_id=user_id, quest_id=quest_id).order_by(UserQuest.id.desc()).first()
    if not submission or (submission.status != 'rejected' and submission.verification_status != 'rejected'):
        return jsonify({'error': 'No rejected submission found for this quest.'}), 400

    submission.status = 'pending'
    submission.verification_status = 'pending'
    submission.submission_link = None
    submission.submission_text = None
    submission.submitted_at = None
    submission.admin_notes = None
    submission.proof_data = None
    submission.completed_at = None

    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Acknowledged. You can submit new proof now.'})

@quests_bp.route('/verify-telegram/<int:quest_id>', methods=['POST'])
def verify_telegram_membership(quest_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    quest = Quest.query.get_or_404(quest_id)
    user = User.query.get(user_id)

    if quest.quest_type != 'telegram':
        return jsonify({'error': 'Invalid quest type'}), 400

    # Check if already completed
    existing = UserQuest.query.filter_by(user_id=user_id, quest_id=quest_id, status='completed').first()
    if existing:
        return jsonify({'success': True, 'message': 'Already completed', 'points': quest.points, 'new_total_points': user.points})

    latest_submission = UserQuest.query.filter_by(user_id=user_id, quest_id=quest_id).order_by(UserQuest.id.desc()).first()

    def award_success(submission):
        if submission:
            submission.status = 'completed'
            submission.verification_status = 'verified'
            submission.completed_at = datetime.utcnow()
        else:
            db.session.add(UserQuest(
                user_id=user_id,
                quest_id=quest_id,
                status='completed',
                verification_status='verified',
                completed_at=datetime.utcnow()
            ))
        user.points += quest.points
        user.xp += quest.points
        db.session.commit()
        return jsonify({
            'success': True,
            'points': quest.points,
            'new_total_points': user.points
        })

    platform_config = quest.platform_config or {}
    require_bot = True
    if 'telegram_bot_verify' in platform_config:
        flag = platform_config.get('telegram_bot_verify')
        if isinstance(flag, str):
            require_bot = flag.strip().lower() in ('1', 'true', 'yes', 'on', 'y')
        else:
            require_bot = bool(flag)

    if not require_bot:
        return award_success(latest_submission)

    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = platform_config.get('chat_id') if isinstance(platform_config, dict) else None
    if not chat_id:
        chat_id = quest.verification_data

    if not bot_token or not chat_id:
        return jsonify({'error': 'Server configuration error (Missing Token or Chat ID)'}), 500

    if not user.telegram_id:
        return jsonify({'error': 'Your account is not linked to Telegram.'}), 400

    try:
        url = f"https://api.telegram.org/bot{bot_token}/getChatMember"
        params = {'chat_id': chat_id, 'user_id': user.telegram_id}

        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()

        if not data.get('ok'):
            return jsonify({'error': f"Telegram API Error: {data.get('description')}"}), 400

        result = data.get('result', {})
        status = result.get('status')
        valid_statuses = ['member', 'administrator', 'creator', 'restricted']

        if status not in valid_statuses:
            return jsonify({'error': 'You are not a member of the group/channel yet. Please join and try again.'}), 400

        member_user = result.get('user') or {}
        member_username = member_user.get('username')
        if user.username and member_username and user.username.lower() != member_username.lower():
            return jsonify({'error': 'Telegram username mismatch. Please verify you joined with the correct account.'}), 400
        if not user.username and member_username:
            user.username = member_username

        return award_success(latest_submission)

    except Exception as e:
        return jsonify({'error': f"Verification failed: {str(e)}"}), 500

@quests_bp.route('/checkin/<int:quest_id>', methods=['POST'])
def checkin_quest(quest_id):
    """Handle daily check-in for a quest"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    quest = Quest.query.get_or_404(quest_id)
    
    # Verify this is a daily check-in quest
    if quest.quest_type != 'daily_checkin':
        return jsonify({'error': 'Not a daily check-in quest'}), 400
    
    user = User.query.get(user_id)
    today = date.today()
    
    # Check if already checked in today
    existing_checkin = DailyCheckIn.query.filter_by(
        user_id=user_id,
        quest_id=quest_id,
        check_in_date=today
    ).first()
    
    if existing_checkin:
        return jsonify({
            'error': 'Already checked in today',
            'streak': existing_checkin.streak_count
        }), 400
    
    # Get yesterday's check-in to calculate streak
    yesterday = today - timedelta(days=1)
    yesterday_checkin = DailyCheckIn.query.filter_by(
        user_id=user_id,
        quest_id=quest_id,
        check_in_date=yesterday
    ).first()
    
    # Calculate streak
    if yesterday_checkin:
        streak_count = yesterday_checkin.streak_count + 1
    else:
        streak_count = 1
    
    # Create check-in record
    checkin = DailyCheckIn(
        user_id=user_id,
        quest_id=quest_id,
        check_in_date=today,
        streak_count=streak_count
    )
    db.session.add(checkin)
    
    # Award points
    user.points += quest.points
    user.xp += quest.points
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'streak': streak_count,
        'points_earned': quest.points,
        'new_total_points': user.points
    })
