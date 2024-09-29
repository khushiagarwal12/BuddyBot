from flask import Flask, request, jsonify, send_from_directory
import os
import random
import google.generativeai as genai

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyBm0Ajs-y1nLXoJ3y3PQF64i2OC8LO3pUU"
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/send', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    
    empathetic_responses = {
        "stress": "I understand that stress can be overwhelming. Remember to take deep breaths and focus on what you can control. You're doing great!",
        "exam": "Exams can be nerve-wracking, but I believe in you! Remember to take breaks and be kind to yourself during your study sessions.",
        "friend": "Friendship issues can be tough. It's okay to feel upset, and remember that communication is key in resolving conflicts.",
        "homesick": "Feeling homesick is completely normal. It's okay to miss home, and remember that it's just a sign of how much you care about your loved ones.",
        "tired": "It's important to listen to your body. Make sure you're getting enough rest and don't hesitate to take breaks when you need them.",
        "help": "I'm here to support you in any way I can. Feel free to share what's on your mind, and we can work through it together.",
    }

    for keyword, response in empathetic_responses.items():
        if keyword in user_message.lower():
            return jsonify({"response": response})

    chat_session = model.start_chat(history=[])
    
    prompt = f"You are BuddyBot, an empathetic AI assistant for students. Respond to the following message in a supportive, encouraging, and student-friendly manner: {user_message}"
    
    response = chat_session.send_message(prompt)
    bot_response = response.text
    
    supportive_closings = [
        "Remember, I'm always here to listen and support you!",
        "You're doing great, and I believe in you!",
        "Don't hesitate to reach out if you need more support or just want to chat.",
        "Take care of yourself, and remember that you're capable of amazing things!",
    ]
    bot_response += f" {random.choice(supportive_closings)}"

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
