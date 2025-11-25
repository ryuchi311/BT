from flask import Blueprint, render_template, jsonify, request, session
from models import db, Reward, UserReward, User
from datetime import datetime

rewards_bp = Blueprint('rewards', __name__, url_prefix='/rewards')

@rewards_bp.route('/')
def list_rewards():
    """Display all active rewards"""
    user_id = session.get('user_id')
    user = None
    if user_id:
        user = User.query.get(user_id)
    
    # Get all active rewards
    rewards = Reward.query.filter_by(is_active=True).all()
    
    return render_template('rewards.html', rewards=rewards, user=user)

@rewards_bp.route('/claim/<int:reward_id>', methods=['POST'])
def claim_reward(reward_id):
    """Handle reward claiming"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(user_id)
    reward = Reward.query.get_or_404(reward_id)
    
    # Check if reward is active
    if not reward.is_active:
        return jsonify({'error': 'Reward is not available'}), 400
    
    # Check stock availability
    if reward.stock is not None and reward.stock <= 0:
        return jsonify({'error': 'Reward is out of stock'}), 400
    
    # Check if user has enough points
    if user.points < reward.cost:
        return jsonify({
            'error': 'Insufficient points',
            'required': reward.cost,
            'current': user.points
        }), 400
    
    # Deduct points
    user.points -= reward.cost
    
    # Decrement stock if limited
    if reward.stock is not None:
        reward.stock -= 1
    
    # Create claim record
    user_reward = UserReward(
        user_id=user_id,
        reward_id=reward_id,
        status='pending'
    )
    db.session.add(user_reward)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'reward_title': reward.title,
        'points_spent': reward.cost,
        'remaining_points': user.points,
        'claim_id': user_reward.id
    })

@rewards_bp.route('/history')
def claim_history():
    """Show user's claimed rewards"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(user_id)
    claims = UserReward.query.filter_by(user_id=user_id).order_by(UserReward.claimed_at.desc()).all()
    
    return render_template('reward_history.html', claims=claims, user=user)
