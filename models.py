from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    photo_url = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(128), nullable=True)  # User email for onboarding
    is_onboarded = db.Column(db.Boolean, default=False)  # Has completed onboarding
    terms_accepted = db.Column(db.Boolean, default=False)  # Has accepted terms
    terms_accepted_at = db.Column(db.DateTime)  # When terms were accepted
    xp = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    quests = db.relationship('UserQuest', foreign_keys='UserQuest.user_id', backref='user', lazy='dynamic')

    def to_dict(self):
        """Serialize commonly needed user attributes for JSON responses."""
        return {
            'id': self.id,
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo_url': self.photo_url,
            'email': self.email,
            'is_onboarded': self.is_onboarded,
            'terms_accepted': self.terms_accepted,
            'xp': self.xp,
            'points': self.points
        }

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    quest_type = db.Column(db.String(32), nullable=False) # telegram, twitter, youtube, visit, daily_checkin
    points = db.Column(db.Integer, default=10)
    verification_data = db.Column(db.String(256)) # Link to verify or channel ID
    icon = db.Column(db.String(64), default='star') # Icon name for UI
    action_url = db.Column(db.String(256)) # URL to perform the action
    category = db.Column(db.String(64)) # Social, Engagement, Educational, Reward
    expires_at = db.Column(db.DateTime) # Expiration date/time
    is_active = db.Column(db.Boolean, default=True) # Active status
    
    # Platform-specific configuration
    platform_config = db.Column(db.JSON) # Platform-specific settings (channel_id, account, etc.)
    verification_type = db.Column(db.String(50), default='auto') # 'auto', 'manual', 'proof_required'
    verification_instructions = db.Column(db.Text) # Instructions for users on how to complete/verify
    verification_code = db.Column(db.String(32), nullable=True) # Code for YouTube quest verification

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'points': self.points,
            'quest_type': self.quest_type,
            'icon': self.icon,
            'action_url': self.action_url,
            'verification_data': self.verification_data,
            'verification_code': self.verification_code,
            'category': self.category,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active
        }

class UserQuest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, submitted, approved, rejected
    completed_at = db.Column(db.DateTime)
    
    # Submission tracking fields
    submission_text = db.Column(db.Text)
    submission_link = db.Column(db.String(512))
    submitted_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_at = db.Column(db.DateTime)
    
    # Verification proof data
    proof_data = db.Column(db.JSON) # Store URLs, file paths, verification info
    verification_status = db.Column(db.String(20), default='pending') # 'pending', 'verified', 'rejected'
    admin_notes = db.Column(db.Text) # Admin notes for manual verification
    
    # Relationships
    quest = db.relationship('Quest', backref='user_quests')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    cost = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(256))
    stock = db.Column(db.Integer, nullable=True)  # NULL = unlimited
    is_active = db.Column(db.Boolean, default=True)
    category = db.Column(db.String(64))  # Physical, Digital, Voucher, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'cost': self.cost,
            'image_url': self.image_url,
            'stock': self.stock,
            'is_active': self.is_active,
            'category': self.category
        }

class SystemSetting(db.Model):
    key = db.Column(db.String(128), primary_key=True)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DailyCheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)  # Date only (no time)
    streak_count = db.Column(db.Integer, default=1)  # Current consecutive days
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='check_ins')
    quest = db.relationship('Quest', backref='check_ins')
    
    # Unique constraint: one check-in per user per quest per day
    __table_args__ = (
        db.UniqueConstraint('user_id', 'quest_id', 'check_in_date', name='unique_daily_checkin'),
    )

class UserReward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reward_id = db.Column(db.Integer, db.ForeignKey('reward.id'), nullable=False)
    claimed_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, shipped, delivered, cancelled
    delivery_info = db.Column(db.Text)  # JSON string for address/contact info
    
    # Relationships
    user = db.relationship('User', backref='claimed_rewards')
    reward = db.relationship('Reward', backref='claims')
