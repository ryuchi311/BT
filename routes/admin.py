from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Quest, SystemSetting, UserQuest, User, Reward, UserReward
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    quests = Quest.query.order_by(Quest.id.desc()).all()
    quests_data = [q.to_dict() for q in quests]
    return render_template('admin_dashboard.html', quests=quests, quests_data=quests_data)

@admin_bp.route('/quest/add', methods=['POST'])
def add_quest():
    title = request.form.get('title')
    description = request.form.get('description')
    points = int(request.form.get('points'))
    platform = request.form.get('platform')
    category = request.form.get('category')
    action_url = request.form.get('action_url')
    verification_data = request.form.get('verification_data')
    expires_at_str = request.form.get('expires_at')
    
    # Parse expiration date if provided
    expires_at = None
    if expires_at_str:
        try:
            expires_at = datetime.fromisoformat(expires_at_str)
        except ValueError:
            pass
    
    quest = Quest(
        title=title,
        description=description,
        points=points,
        quest_type=platform,
        category=category,
        action_url=action_url,
        verification_data=verification_data,
        verification_code=request.form.get('verification_code') or None,
        expires_at=expires_at,
        is_active=True
    )
    
    db.session.add(quest)
    db.session.commit()
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/quest/edit/<int:quest_id>', methods=['POST'])
def edit_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    
    quest.title = request.form.get('title')
    quest.description = request.form.get('description')
    quest.points = int(request.form.get('points'))
    quest.quest_type = request.form.get('platform')
    quest.category = request.form.get('category')
    quest.action_url = request.form.get('action_url')
    quest.verification_data = request.form.get('verification_data')
    # Save verification_code (used for YouTube quests)
    quest.verification_code = request.form.get('verification_code') or None
    
    expires_at_str = request.form.get('expires_at')
    if expires_at_str:
        try:
            quest.expires_at = datetime.fromisoformat(expires_at_str)
        except ValueError:
            quest.expires_at = None
    else:
        quest.expires_at = None
    
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/quest/delete/<int:quest_id>', methods=['POST'])
def delete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    db.session.delete(quest)
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/quest/toggle/<int:quest_id>', methods=['POST'])
def toggle_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    quest.is_active = not quest.is_active
    db.session.commit()
    return jsonify({'success': True})

# Verification Queue Routes
@admin_bp.route('/verification-queue')
def verification_queue():
    # Get all submitted quests pending review
    pending_submissions = db.session.query(UserQuest, User, Quest).join(
        User, UserQuest.user_id == User.id
    ).join(
        Quest, UserQuest.quest_id == Quest.id
    ).filter(
        UserQuest.status == 'submitted'
    ).order_by(
        UserQuest.submitted_at.desc()
    ).all()
    
    return render_template('verification_queue.html', submissions=pending_submissions)

@admin_bp.route('/verify/approve/<int:submission_id>', methods=['POST'])
def approve_submission(submission_id):
    submission = UserQuest.query.get_or_404(submission_id)
    quest = Quest.query.get(submission.quest_id)
    user = User.query.get(submission.user_id)
    
    # Update submission status
    submission.status = 'approved'
    submission.completed_at = datetime.utcnow()
    submission.reviewed_at = datetime.utcnow()
    # Note: reviewed_by would need admin user ID - for now we'll leave it null
    
    # Award points to user
    user.points += quest.points
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Submission approved'})

@admin_bp.route('/verify/reject/<int:submission_id>', methods=['POST'])
def reject_submission(submission_id):
    submission = UserQuest.query.get_or_404(submission_id)
    
    # Update submission status
    submission.status = 'rejected'
    submission.reviewed_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Submission rejected'})

# ===== REWARD MANAGEMENT ROUTES =====

@admin_bp.route('/rewards')
def manage_rewards():
    """Admin reward management page"""
    rewards = Reward.query.all()
    rewards_data = [r.to_dict() for r in rewards]
    return render_template('admin_rewards.html', rewards=rewards, rewards_data=rewards_data)

@admin_bp.route('/rewards/add', methods=['POST'])
def add_reward():
    """Create a new reward"""
    title = request.form.get('title')
    description = request.form.get('description')
    cost = int(request.form.get('cost'))
    image_url = request.form.get('image_url')
    category = request.form.get('category')
    stock_str = request.form.get('stock')
    
    # Parse stock (empty = unlimited)
    stock = None
    if stock_str and stock_str.strip():
        stock = int(stock_str)
    
    reward = Reward(
        title=title,
        description=description,
        cost=cost,
        image_url=image_url,
        category=category,
        stock=stock,
        is_active=True
    )
    
    db.session.add(reward)
    db.session.commit()
    
    return redirect(url_for('admin.manage_rewards'))

@admin_bp.route('/rewards/edit/<int:reward_id>', methods=['POST'])
def edit_reward(reward_id):
    """Edit an existing reward"""
    reward = Reward.query.get_or_404(reward_id)
    
    reward.title = request.form.get('title')
    reward.description = request.form.get('description')
    reward.cost = int(request.form.get('cost'))
    reward.image_url = request.form.get('image_url')
    reward.category = request.form.get('category')
    
    stock_str = request.form.get('stock')
    reward.stock = int(stock_str) if stock_str and stock_str.strip() else None
    
    db.session.commit()
    
    return redirect(url_for('admin.manage_rewards'))

@admin_bp.route('/rewards/toggle/<int:reward_id>', methods=['POST'])
def toggle_reward(reward_id):
    """Toggle reward active status"""
    reward = Reward.query.get_or_404(reward_id)
    reward.is_active = not reward.is_active
    db.session.commit()
    return jsonify({'success': True})

@admin_bp.route('/rewards/delete/<int:reward_id>', methods=['POST'])
def delete_reward(reward_id):
    """Delete a reward"""
    reward = Reward.query.get_or_404(reward_id)
    db.session.delete(reward)
    db.session.commit()
    return jsonify({'success': True})
