from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import get_config
from database import init_db, Session
from routes.auth import auth_bp
from routes.companion import companion_bp
from models.companion import Companion
from services.activity_simulator import ActivitySimulator
from services.companion_ai import CompanionAI

# Initialize Flask app
app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(companion_bp, url_prefix='/api/companion')

# Root endpoint
@app.route('/')
def index():
    return jsonify({
        'message': 'Nojudge AI Companion API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'companion': '/api/companion'
        }
    })

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'message': 'Connected to Nojudge server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_activity_update')
def handle_activity_update(data):
    """Client requests activity update for their companion"""
    try:
        user_id = data.get('user_id')
        if not user_id:
            emit('error', {'message': 'User ID required'})
            return
        
        db = Session()
        companion = db.query(Companion).filter_by(user_id=user_id).first()
        
        if companion:
            # Check for activity changes
            should_change, new_activity = ActivitySimulator.should_start_new_activity(companion)
            
            if should_change and new_activity:
                ai = CompanionAI(companion)
                announcement = ai.get_activity_announcement(new_activity)
                companion.start_activity(new_activity)
                db.commit()
                
                emit('activity_changed', {
                    'activity': new_activity,
                    'announcement': announcement,
                    'companion_state': companion.to_dict()
                })
            else:
                emit('activity_update', {
                    'activity': companion.current_activity,
                    'companion_state': companion.to_dict()
                })
        
        db.close()
        
    except Exception as e:
        emit('error', {'message': str(e)})

# Initialize database
with app.app_context():
    print("Initializing database...")
    init_db()
    print("Database initialized!")

if __name__ == '__main__':
    print("Starting Nojudge AI Companion Server...")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Debug mode: {config.DEBUG}")
    
    # Run with standard Flask development server
    # For production, use a proper WSGI server like gunicorn
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=config.DEBUG
    )
