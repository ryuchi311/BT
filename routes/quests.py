from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from models import db, Quest, UserQuest, User, DailyCheckIn
from datetime import datetime, date, timedelta

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
    
    return render_template('quests.html', quests=quests, checkin_status=checkin_status)

@quests_bp.route('/complete/<int:quest_id>', methods=['POST'])
def complete_quest(quest_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    # Check if already completed
    existing = UserQuest.query.filter_by(user_id=user_id, quest_id=quest_id).first()
    if existing and existing.status == 'completed':
        return jsonify({'error': 'Already completed'}), 400
        
    quest = Quest.query.get_or_404(quest_id)
    user = User.query.get(user_id)
    
    # Here we would add specific verification logic based on quest.quest_type
    # For prototype, we assume instant completion
    
    if not existing:
        uq = UserQuest(user_id=user_id, quest_id=quest_id, status='completed')
        db.session.add(uq)
    else:
        existing.status = 'completed'
        
    user.points += quest.points
    user.xp += quest.points # 1 point = 1 XP for now
    
    db.session.commit()
    
    return jsonify({'status': 'success', 'new_points': user.points})

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
