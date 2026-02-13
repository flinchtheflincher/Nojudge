from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import random

class Companion(Base):
    __tablename__ = 'companions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    name = Column(String(100), default='Nojudge')
    
    # Personality types: intelligent, lazy, inquisitive, cheerful, grumpy, curious
    personality_type = Column(String(50), default='curious')
    
    # Current state: idle, cooking, eating, sleeping, thinking, exploring
    current_activity = Column(String(50), default='idle')
    
    # Mood: 0-100 scale
    mood = Column(Float, default=75.0)
    
    # Energy level: 0-100 scale
    energy_level = Column(Float, default=80.0)
    
    last_activity_time = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship('User', backref='companion')
    
    def update_mood(self, change):
        """Update mood with bounds checking"""
        self.mood = max(0, min(100, self.mood + change))
    
    def update_energy(self, change):
        """Update energy with bounds checking"""
        self.energy_level = max(0, min(100, self.energy_level + change))
    
    def start_activity(self, activity):
        """Start a new activity"""
        self.current_activity = activity
        self.last_activity_time = datetime.utcnow()
        
        # Activities affect energy and mood
        if activity == 'eating':
            self.update_energy(15)
            self.update_mood(10)
        elif activity == 'sleeping':
            self.update_energy(30)
        elif activity == 'cooking':
            self.update_energy(-5)
            self.update_mood(5)
        elif activity == 'exploring':
            self.update_energy(-10)
            self.update_mood(15)
    
    def get_personality_traits(self):
        """Get personality description"""
        traits = {
            'intelligent': 'Smart and analytical, loves solving problems',
            'lazy': 'Relaxed and easygoing, prefers minimal effort',
            'inquisitive': 'Curious and questioning, always wants to learn',
            'cheerful': 'Happy and optimistic, spreads positive vibes',
            'grumpy': 'A bit cranky but lovable, honest and direct',
            'curious': 'Interested in everything, loves exploring'
        }
        return traits.get(self.personality_type, 'Unique and special')
    
    def to_dict(self):
        """Convert companion to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'personality_type': self.personality_type,
            'personality_description': self.get_personality_traits(),
            'current_activity': self.current_activity,
            'mood': round(self.mood, 1),
            'energy_level': round(self.energy_level, 1),
            'last_activity_time': self.last_activity_time.isoformat() if self.last_activity_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
