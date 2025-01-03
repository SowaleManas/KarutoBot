import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the conversation history from the request body
        messages = request.json.get('messages', [])
        if not messages:
            return jsonify({"reply": "No messages provided. Please try again."}), 400

        # Use the OpenAI client to create a chat completion
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-4",
            max_tokens=150,
            temperature=0.8
        )

        # Access the reply using dot notation
        bot_reply = chat_completion.choices[0].message.content.strip()
        return jsonify({"reply": bot_reply})

    except Exception as e:
        # Handle errors gracefully
        print(f"Error: {e}")
        return jsonify({"reply": "Something went wrong. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)
