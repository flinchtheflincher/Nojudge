from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    companion_id = Column(Integer, ForeignKey('companions.id'), nullable=False)
    
    # True if message is from user, False if from companion
    is_user_message = Column(Boolean, nullable=False)
    
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    companion = relationship('Companion', backref='messages')
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'companion_id': self.companion_id,
            'is_user_message': self.is_user_message,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
