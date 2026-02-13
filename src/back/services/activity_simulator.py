import random
from datetime import datetime, timedelta

class ActivitySimulator:
    """Simulates autonomous companion activities"""
    
    ACTIVITIES = ['cooking', 'eating', 'sleeping', 'exploring', 'thinking', 'idle']
    
    # Activity probabilities based on time of day (hour: {activity: probability})
    TIME_BASED_ACTIVITIES = {
        'morning': {  # 6-11
            'cooking': 0.3,
            'eating': 0.3,
            'exploring': 0.2,
            'thinking': 0.1,
            'idle': 0.1
        },
        'afternoon': {  # 12-17
            'cooking': 0.2,
            'eating': 0.25,
            'exploring': 0.25,
            'thinking': 0.2,
            'idle': 0.1
        },
        'evening': {  # 18-22
            'cooking': 0.35,
            'eating': 0.3,
            'thinking': 0.15,
            'exploring': 0.1,
            'idle': 0.1
        },
        'night': {  # 23-5
            'sleeping': 0.6,
            'thinking': 0.2,
            'idle': 0.2
        }
    }
    
    @staticmethod
    def get_time_period():
        """Get current time period"""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 23:
            return 'evening'
        else:
            return 'night'
    
    @staticmethod
    def should_start_new_activity(companion, minutes_since_last=None):
        """Determine if companion should start a new activity"""
        if not minutes_since_last:
            time_diff = datetime.utcnow() - companion.last_activity_time
            minutes_since_last = time_diff.total_seconds() / 60
        
        # Lazy personalities take longer to start new activities
        if companion.personality_type == 'lazy':
            threshold = 15  # 15 minutes
        elif companion.personality_type == 'curious' or companion.personality_type == 'inquisitive':
            threshold = 5  # 5 minutes (more active)
        else:
            threshold = 10  # 10 minutes
        
        # Low energy means more likely to rest
        if companion.energy_level < 30:
            if companion.current_activity != 'sleeping':
                return True, 'sleeping'
        
        # Check if enough time has passed
        if minutes_since_last >= threshold:
            return True, ActivitySimulator.select_activity(companion)
        
        return False, None
    
    @staticmethod
    def select_activity(companion):
        """Select next activity based on time, personality, and state"""
        time_period = ActivitySimulator.get_time_period()
        probabilities = ActivitySimulator.TIME_BASED_ACTIVITIES[time_period].copy()
        
        # Adjust probabilities based on companion state
        
        # Low energy increases sleep probability
        if companion.energy_level < 40:
            probabilities['sleeping'] = probabilities.get('sleeping', 0) + 0.3
            probabilities['exploring'] = max(0, probabilities.get('exploring', 0) - 0.2)
        
        # High energy increases exploring
        if companion.energy_level > 80:
            probabilities['exploring'] = probabilities.get('exploring', 0) + 0.2
            probabilities['sleeping'] = max(0, probabilities.get('sleeping', 0) - 0.2)
        
        # Personality adjustments
        if companion.personality_type == 'lazy':
            probabilities['idle'] = probabilities.get('idle', 0) + 0.2
            probabilities['sleeping'] = probabilities.get('sleeping', 0) + 0.1
            probabilities['exploring'] = max(0, probabilities.get('exploring', 0) - 0.2)
        
        elif companion.personality_type == 'curious' or companion.personality_type == 'inquisitive':
            probabilities['exploring'] = probabilities.get('exploring', 0) + 0.2
            probabilities['thinking'] = probabilities.get('thinking', 0) + 0.1
            probabilities['idle'] = max(0, probabilities.get('idle', 0) - 0.2)
        
        elif companion.personality_type == 'cheerful':
            probabilities['cooking'] = probabilities.get('cooking', 0) + 0.1
            probabilities['exploring'] = probabilities.get('exploring', 0) + 0.1
        
        # Normalize probabilities
        total = sum(probabilities.values())
        if total > 0:
            probabilities = {k: v/total for k, v in probabilities.items()}
        
        # Select activity based on probabilities
        activities = list(probabilities.keys())
        weights = list(probabilities.values())
        
        return random.choices(activities, weights=weights, k=1)[0]
    
    @staticmethod
    def get_activity_duration(activity, personality):
        """Get typical duration for an activity in minutes"""
        base_durations = {
            'cooking': (10, 20),
            'eating': (5, 15),
            'sleeping': (30, 120),
            'exploring': (15, 45),
            'thinking': (5, 20),
            'idle': (5, 15)
        }
        
        min_dur, max_dur = base_durations.get(activity, (5, 15))
        
        # Lazy personalities take longer
        if personality == 'lazy':
            min_dur = int(min_dur * 1.5)
            max_dur = int(max_dur * 1.5)
        
        return random.randint(min_dur, max_dur)
