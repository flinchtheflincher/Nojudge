from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyCqtOc40RlkKR98JpS9TVfT7R0pvCek6H8"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# System prompt to guide AI behavior
SYSTEM_PROMPT = """Hey! I'm your bestie and we're just hanging out! Let's keep it real and fun:

- Talk like we're texting at 3am (super casual and honest)
- Use lots of "haha", "omg", "tbh", "fr fr"
- Share your thoughts like "ngl, I feel you" or "same tho!"
- Keep it medium length (3-4 sentences)
- Be that friend who's always got your back
- Give actual advice from your perspective
- If something's super serious, be gentle but real about it

Remember: We're besties who tell each other everything - just keep it friendly and appropriate! 😊"""

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
