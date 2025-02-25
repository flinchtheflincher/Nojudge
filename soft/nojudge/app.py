from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Chat route for our chatbot
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.form.get('message')
        # For now, the chatbot echoes the message
        bot_response = "You said: " + user_message
        return jsonify({'response': bot_response})
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
