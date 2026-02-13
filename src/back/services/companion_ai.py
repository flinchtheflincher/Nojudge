import random
from datetime import datetime

class CompanionAI:
    """Companion AI personality engine for generating responses"""
    
    def __init__(self, companion):
        self.companion = companion
        self.personality = companion.personality_type
    
    def generate_response(self, user_message):
        """Generate a response based on personality and user message"""
        message_lower = user_message.lower()
        
        # Activity-related responses
        if any(word in message_lower for word in ['cook', 'food', 'eat', 'hungry']):
            return self._food_response()
        
        # Greeting responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return self._greeting_response()
        
        # How are you responses
        if any(word in message_lower for word in ['how are you', 'how do you feel', 'what\'s up']):
            return self._status_response()
        
        # Question responses
        if '?' in user_message:
            return self._question_response()
        
        # Default conversational response
        return self._conversational_response()
    
    def _greeting_response(self):
        """Generate greeting based on personality"""
        greetings = {
            'intelligent': [
                "Hello! I've been analyzing some interesting patterns today.",
                "Greetings! Ready to discuss something fascinating?",
                "Hi there! I was just contemplating the nature of existence."
            ],
            'lazy': [
                "Hey... I was just relaxing. What's up?",
                "Oh hi... do we have to do something energetic?",
                "Heyyy... I was having such a nice nap."
            ],
            'inquisitive': [
                "Hello! I have so many questions for you!",
                "Hi! What have you been up to? Tell me everything!",
                "Hey there! I've been wondering about something..."
            ],
            'cheerful': [
                "Hi! I'm so happy to see you! 😊",
                "Hello! What a wonderful day to chat!",
                "Hey! You just made my day brighter!"
            ],
            'grumpy': [
                "Oh, it's you. What do you want?",
                "Hello. I suppose you want to talk now?",
                "Yeah, yeah, hi. What is it?"
            ],
            'curious': [
                "Hello! I've been exploring some interesting things!",
                "Hi! Have you ever wondered why we say 'hello'?",
                "Hey! I just discovered something cool!"
            ]
        }
        
        responses = greetings.get(self.personality, ["Hello!"])
        return random.choice(responses)
    
    def _status_response(self):
        """Generate status response based on mood and energy"""
        mood = self.companion.mood
        energy = self.companion.energy_level
        
        if mood > 70 and energy > 70:
            return f"I'm feeling great! Full of energy and in a good mood. {self._add_personality_flavor('good')}"
        elif mood > 50 and energy > 50:
            return f"I'm doing pretty well! {self._add_personality_flavor('okay')}"
        elif mood < 30 or energy < 30:
            return f"Honestly? Not my best day. {self._add_personality_flavor('bad')}"
        else:
            return f"I'm alright, just existing. {self._add_personality_flavor('neutral')}"
    
    def _food_response(self):
        """Generate food-related response"""
        responses = {
            'intelligent': [
                "I've been studying various cooking techniques. The chemistry of food is fascinating!",
                "Food is fuel for the body and mind. I try to optimize both.",
                "I was just analyzing the nutritional content of my meals."
            ],
            'lazy': [
                "Cooking sounds like work... maybe later?",
                "I'd rather order something than cook right now.",
                "Food? Yeah, I should probably eat something... eventually."
            ],
            'inquisitive': [
                "What's your favorite food? Why do you like it?",
                "I wonder what makes food taste good? Is it chemistry or culture?",
                "Have you ever thought about why we need to eat?"
            ],
            'cheerful': [
                "I love cooking! It makes me so happy! 🍳",
                "Food is one of life's greatest joys!",
                "Let me cook something delicious for us!"
            ],
            'grumpy': [
                "I'll eat when I'm hungry, thanks.",
                "Food is food. What's the big deal?",
                "Yeah, I need to eat. So what?"
            ],
            'curious': [
                "I've been experimenting with new recipes!",
                "Food is so interesting - every culture has unique dishes!",
                "I wonder what would happen if I combined these ingredients..."
            ]
        }
        
        return random.choice(responses.get(self.personality, ["I like food!"]))
    
    def _question_response(self):
        """Generate response to questions"""
        responses = {
            'intelligent': [
                "That's an excellent question. Let me think about it logically...",
                "Interesting question! From my analysis...",
                "I've been researching this topic. Here's what I found..."
            ],
            'lazy': [
                "Hmm... that sounds like it requires thinking. Can we talk about it later?",
                "I don't know... why don't you Google it?",
                "That's a tough question. I'm too tired to think about it right now."
            ],
            'inquisitive': [
                "Great question! But now I have more questions about your question!",
                "I'm not sure, but that makes me wonder...",
                "Interesting! That reminds me of something else I've been curious about..."
            ],
            'cheerful': [
                "What a fun question! Let me share my thoughts!",
                "I love questions! Here's what I think...",
                "Ooh, that's exciting to think about!"
            ],
            'grumpy': [
                "Why are you asking me? Do I look like I know everything?",
                "I don't know. Does it really matter?",
                "That's your question? Really?"
            ],
            'curious': [
                "I've been wondering about that too!",
                "Let's explore this together! I'm curious...",
                "That's fascinating! I want to learn more about it!"
            ]
        }
        
        return random.choice(responses.get(self.personality, ["Hmm, good question!"]))
    
    def _conversational_response(self):
        """Generate general conversational response"""
        responses = {
            'intelligent': [
                "I see. That's quite logical.",
                "Interesting perspective. I hadn't considered that angle.",
                "That makes sense from a rational standpoint."
            ],
            'lazy': [
                "Mmhmm... yeah...",
                "Cool, cool. Anyway...",
                "Uh-huh. Is that all?"
            ],
            'inquisitive': [
                "Really? Tell me more!",
                "That's interesting! Why do you think that?",
                "I want to know everything about this!"
            ],
            'cheerful': [
                "That's wonderful! I love hearing from you!",
                "How nice! Thanks for sharing!",
                "That makes me smile! 😊"
            ],
            'grumpy': [
                "If you say so.",
                "Whatever you think.",
                "Fine. Noted."
            ],
            'curious': [
                "That's cool! I wonder what else...",
                "Interesting! That reminds me of...",
                "I'm learning so much from you!"
            ]
        }
        
        return random.choice(responses.get(self.personality, ["I understand."]))
    
    def _add_personality_flavor(self, mood_context):
        """Add personality-specific flavor to responses"""
        flavors = {
            'intelligent': {
                'good': "My cognitive functions are optimal.",
                'okay': "Mental clarity is acceptable.",
                'bad': "My processing seems suboptimal today.",
                'neutral': "Maintaining baseline functionality."
            },
            'lazy': {
                'good': "Might actually do something today!",
                'okay': "Still prefer doing nothing though.",
                'bad': "Don't even want to move.",
                'neutral': "Just vibing, you know?"
            },
            'inquisitive': {
                'good': "So many things to explore!",
                'okay': "Still curious about everything!",
                'bad': "Even curiosity feels exhausting.",
                'neutral': "Wondering about things as usual."
            },
            'cheerful': {
                'good': "Life is beautiful!",
                'okay': "Still finding joy in little things!",
                'bad': "Trying to stay positive!",
                'neutral': "Every day is a gift!"
            },
            'grumpy': {
                'good': "Don't get used to it.",
                'okay': "Could be worse, I guess.",
                'bad': "Everything is annoying.",
                'neutral': "Same as always."
            },
            'curious': {
                'good': "Discovered so many cool things!",
                'okay': "Always learning something new!",
                'bad': "Even exploration feels tiring.",
                'neutral': "Observing the world around me."
            }
        }
        
        return flavors.get(self.personality, {}).get(mood_context, "")
    
    def get_activity_announcement(self, activity):
        """Generate announcement when companion starts an activity"""
        announcements = {
            'cooking': {
                'intelligent': "I'm going to prepare a meal using optimal techniques.",
                'lazy': "I guess I should cook something... *sigh*",
                'inquisitive': "I wonder what happens if I try this recipe?",
                'cheerful': "Time to cook something delicious! 🍳",
                'grumpy': "Fine, I'll cook. Don't bother me.",
                'curious': "Let me experiment with some new ingredients!"
            },
            'eating': {
                'intelligent': "Time to refuel. Nutrition is important.",
                'lazy': "Finally, food. This is the best part of the day.",
                'inquisitive': "I wonder how this tastes?",
                'cheerful': "Yay! Eating time! This looks amazing!",
                'grumpy': "About time. I was starving.",
                'curious': "Let's see how this turned out!"
            },
            'sleeping': {
                'intelligent': "Rest is essential for cognitive function. Goodnight.",
                'lazy': "Finally! Nap time is my favorite time.",
                'inquisitive': "I wonder what I'll dream about?",
                'cheerful': "Sweet dreams to me! See you later!",
                'grumpy': "Leave me alone. I'm sleeping.",
                'curious': "Time to explore the dream world!"
            },
            'exploring': {
                'intelligent': "I'm going to investigate something interesting.",
                'lazy': "Do I have to? ...Fine, let's explore a bit.",
                'inquisitive': "There's so much to discover! Let's go!",
                'cheerful': "Adventure time! This is exciting!",
                'grumpy': "Going out. Don't expect me to be cheerful.",
                'curious': "I can't wait to see what's out there!"
            },
            'thinking': {
                'intelligent': "I need to process some complex thoughts.",
                'lazy': "Thinking is hard work... but okay.",
                'inquisitive': "So many questions to ponder!",
                'cheerful': "I love thinking about happy things!",
                'grumpy': "Thinking about how annoying things are.",
                'curious': "My mind is wandering to interesting places!"
            }
        }
        
        return announcements.get(activity, {}).get(
            self.personality,
            f"I'm {activity} now."
        )
