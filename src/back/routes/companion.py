from flask import Blueprint, request, jsonify
from database import Session
from models.companion import Companion
from models.conversation import Message
from services.companion_ai import CompanionAI
from services.activity_simulator import ActivitySimulator
from utils.auth import token_required
from datetime import datetime

companion_bp = Blueprint('companion', __name__)

@companion_bp.route('/', methods=['GET'])
@token_required
def get_companion(user_id):
    """Get companion state"""
    try:
        db = Session()
        companion = db.query(Companion).filter_by(user_id=user_id).first()
        
        if not companion:
            db.close()
            return jsonify({'error': 'Companion not found'}), 404
        
        # Check if companion should start a new activity
        should_change, new_activity = ActivitySimulator.should_start_new_activity(companion)
        
        if should_change and new_activity:
            companion.start_activity(new_activity)
            db.commit()
        
        response_data = companion.to_dict()
        db.close()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@companion_bp.route('/message', methods=['POST'])
@token_required
def send_message(user_id):
    """Send message to companion and get response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        db = Session()
        companion = db.query(Companion).filter_by(user_id=user_id).first()
        
        if not companion:
            db.close()
            return jsonify({'error': 'Companion not found'}), 404
        
        # Save user message
        user_msg = Message(
            companion_id=companion.id,
            is_user_message=True,
            content=user_message
        )
        db.add(user_msg)
        
        # Generate companion response
        ai = CompanionAI(companion)
        companion_response = ai.generate_response(user_message)
        
        # Save companion response
        companion_msg = Message(
            companion_id=companion.id,
            is_user_message=False,
            content=companion_response
        )
        db.add(companion_msg)
        
        # Update companion mood based on interaction
        companion.update_mood(2)  # Positive interaction
        companion.current_activity = 'idle'  # Companion is now chatting
        companion.last_activity_time = datetime.utcnow()
        
        db.commit()
        
        response_data = {
            'user_message': user_msg.to_dict(),
            'companion_message': companion_msg.to_dict(),
            'companion_state': companion.to_dict()
        }
        
        db.close()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@companion_bp.route('/history', methods=['GET'])
@token_required
def get_conversation_history(user_id):
    """Get conversation history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        db = Session()
        companion = db.query(Companion).filter_by(user_id=user_id).first()
        
        if not companion:
            db.close()
            return jsonify({'error': 'Companion not found'}), 404
        
        # Get recent messages
        messages = db.query(Message)\
            .filter_by(companion_id=companion.id)\
            .order_by(Message.created_at.desc())\
            .limit(limit)\
            .all()
        
        messages.reverse()  # Oldest first
        
        response_data = {
            'messages': [msg.to_dict() for msg in messages],
            'total': len(messages)
        }
        
        db.close()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@companion_bp.route('/activity', methods=['GET'])
@token_required
def get_current_activity(user_id):
    """Get companion's current activity"""
    try:
        db = Session()
        companion = db.query(Companion).filter_by(user_id=user_id).first()
        
        if not companion:
            db.close()
            return jsonify({'error': 'Companion not found'}), 404
        
        # Check for activity changes
        should_change, new_activity = ActivitySimulator.should_start_new_activity(companion)
        
        activity_announcement = None
        if should_change and new_activity:
            ai = CompanionAI(companion)
            activity_announcement = ai.get_activity_announcement(new_activity)
            companion.start_activity(new_activity)
            db.commit()
        
        response_data = {
            'activity': companion.current_activity,
            'mood': companion.mood,
            'energy': companion.energy_level,
            'announcement': activity_announcement,
            'last_activity_time': companion.last_activity_time.isoformat()
        }
        
        db.close()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@companion_bp.route('/trigger-activity', methods=['POST'])
@token_required
def trigger_activity(user_id):
    """Manually trigger an activity (for testing)"""
    try:
        data = request.get_json()
        activity = data.get('activity', '')
        
        valid_activities = ['cooking', 'eating', 'sleeping', 'exploring', 'thinking', 'idle']
        if activity not in valid_activities:
            return jsonify({'error': f'Invalid activity. Must be one of: {valid_activities}'}), 400
        
        db = Session()
        companion = db.query(Companion).filter_by(user_id=user_id).first()
        
        if not companion:
            db.close()
            return jsonify({'error': 'Companion not found'}), 404
        
        # Start activity
        ai = CompanionAI(companion)
        announcement = ai.get_activity_announcement(activity)
        companion.start_activity(activity)
        db.commit()
        
        response_data = {
            'activity': companion.current_activity,
            'announcement': announcement,
            'companion_state': companion.to_dict()
        }
        
        db.close()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
