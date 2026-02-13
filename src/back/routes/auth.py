from flask import Blueprint, request, jsonify
from database import Session
from models.user import User
from models.companion import Companion
from utils.auth import generate_token
import re

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate input
        email = data.get('email', '').strip()
        password = data.get('password', '')
        personality_type = data.get('personality_type', 'curious')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Valid personality types
        valid_personalities = ['intelligent', 'lazy', 'inquisitive', 'cheerful', 'grumpy', 'curious']
        if personality_type not in valid_personalities:
            personality_type = 'curious'
        
        db = Session()
        
        # Check if user already exists
        existing_user = db.query(User).filter_by(email=email).first()
        if existing_user:
            db.close()
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(email=email)
        user.set_password(password)
        db.add(user)
        db.flush()  # Get user ID
        
        # Create companion for user
        companion = Companion(
            user_id=user.id,
            personality_type=personality_type,
            name='Nojudge'
        )
        db.add(companion)
        db.commit()
        
        # Generate token
        token = generate_token(user.id)
        
        db.close()
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': user.to_dict(),
            'companion': companion.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        db = Session()
        
        # Find user
        user = db.query(User).filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            db.close()
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Get companion
        companion = db.query(Companion).filter_by(user_id=user.id).first()
        
        # Generate token
        token = generate_token(user.id)
        
        response_data = {
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict(),
            'companion': companion.to_dict() if companion else None
        }
        
        db.close()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current user info (requires authentication)"""
    from utils.auth import token_required
    
    @token_required
    def _get_user(user_id):
        try:
            db = Session()
            user = db.query(User).filter_by(id=user_id).first()
            
            if not user:
                db.close()
                return jsonify({'error': 'User not found'}), 404
            
            companion = db.query(Companion).filter_by(user_id=user.id).first()
            
            response_data = {
                'user': user.to_dict(),
                'companion': companion.to_dict() if companion else None
            }
            
            db.close()
            return jsonify(response_data), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return _get_user()
