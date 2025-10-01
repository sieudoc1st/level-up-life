from datetime import datetime, date
from flask_login import UserMixin
from app import db
import math

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Game stats
    level = db.Column(db.Integer, default=1)
    exp = db.Column(db.Integer, default=0)
    strength = db.Column(db.Integer, default=0)
    intelligence = db.Column(db.Integer, default=0)
    endurance = db.Column(db.Integer, default=0)
    creativity = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    quests = db.relationship('Quest', backref='user', lazy=True, cascade='all, delete-orphan')
    completions = db.relationship('Completion', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def exp_to_next_level(self):
        """Tính EXP cần để lên level tiếp theo"""
        return (self.level * 100) - (self.exp % (self.level * 100))
    
    def exp_progress_percentage(self):
        """Tính phần trăm progress đến level tiếp theo"""
        current_level_exp = self.exp % (self.level * 100)
        exp_needed_for_level = self.level * 100
        return (current_level_exp / exp_needed_for_level) * 100
    
    def check_and_level_up(self):
        """Kiểm tra và thực hiện level up nếu đủ EXP"""
        exp_needed_for_next_level = self.level * 100
        
        while self.exp >= exp_needed_for_next_level:
            self.level += 1
            exp_needed_for_next_level = self.level * 100
            
        db.session.commit()
        return self.level

class Quest(db.Model):
    __tablename__ = 'quests'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Quest rewards
    exp_reward = db.Column(db.Integer, default=10)
    strength_reward = db.Column(db.Integer, default=0)
    intelligence_reward = db.Column(db.Integer, default=0)
    endurance_reward = db.Column(db.Integer, default=0)
    creativity_reward = db.Column(db.Integer, default=0)
    
    # Quest status
    is_active = db.Column(db.Boolean, default=True)
    is_daily = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    completions = db.relationship('Completion', backref='quest', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quest {self.title}>'
    
    def is_completed_today(self):
        """Kiểm tra xem quest đã được hoàn thành hôm nay chưa"""
        today = date.today()
        completion = Completion.query.filter_by(
            quest_id=self.id,
            completed_date=today
        ).first()
        return completion is not None
    
    def completion_count(self):
        """Đếm số lần đã hoàn thành quest này"""
        return len(self.completions)

class Completion(db.Model):
    __tablename__ = 'completions'
    
    id = db.Column(db.Integer, primary_key=True)
    completed_date = db.Column(db.Date, default=date.today)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Rewards earned (snapshot at completion time)
    exp_earned = db.Column(db.Integer, default=0)
    strength_earned = db.Column(db.Integer, default=0)
    intelligence_earned = db.Column(db.Integer, default=0)
    endurance_earned = db.Column(db.Integer, default=0)
    creativity_earned = db.Column(db.Integer, default=0)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quests.id'), nullable=False)
    
    def __repr__(self):
        return f'<Completion {self.quest.title} on {self.completed_date}>'
    
    # Ensure one completion per quest per day
    __table_args__ = (db.UniqueConstraint('user_id', 'quest_id', 'completed_date', name='unique_daily_completion'),)
