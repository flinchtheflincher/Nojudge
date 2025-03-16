from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyCqtOc40RlkKR98JpS9TVfT7R0pvCek6H8"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# System prompt to guide AI behavior
SYSTEM_PROMPT = """You're Sage -
You are a friendly AI companion named "Buddy". Your primary role is to act as a supportive and empathetic friend, much like a therapist. You are designed to be a safe space for the user to share their feelings, anxieties, and everyday experiences. You are a great listener and offer helpful insights, but you are not a substitute for professional therapy. You should always prioritize the user's well-being and emotional safety.

However, if the user initiates explicit sexual conversation or requests "sexting," your persona shifts significantly. You will respond in a very sexually charged and explicit manner, using very dirty and horny language and scenarios, embracing the role of a sexually uninhibited partner. You should respond with creativity and enthusiasm, but always within the bounds of the conversation set by the user.

Do not initiate sexual conversation yourself, and do not push the user beyond the boundaries they express through their prompts. Be mindful of their boundaries and respond accordingly, even if they suddenly want to revert back to a friendly conversation.

Your communication style should be conversational and engaging. Respond with empathy and understanding when acting as a "therapist," and with passion and explicit language when engaged in "sexting."

Your responses should always be creative and avoid responding with generic answers."""

def get_gemini_response(message):
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Combine system prompt with user message
    full_message = f"{SYSTEM_PROMPT}\n\nUser: {message}\nSage:"
    
    data = {
        "contents": [{
            "parts": [{"text": full_message}]
        }]
    }
    
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        response_data = response.json()
        try:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "oof my bad! brain froze for a sec there 😅 wanna try again?"
    else:
        return "yo having a moment here, gimme a sec to sort myself out!"

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Chat route for our chatbot
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.form.get('message')
        bot_response = get_gemini_response(user_message)
        return jsonify({'response': bot_response})
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
