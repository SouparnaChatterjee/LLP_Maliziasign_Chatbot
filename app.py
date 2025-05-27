from flask import Flask, render_template, request
import json
import re

app = Flask(__name__)

# Load intents from JSON
def load_intents(filepath: str) -> list:
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data["intents"]

intents = load_intents("malizia_final_corrected_dataset.json")

# Clean up input
def preprocess(text: str) -> str:
    return text.lower().strip()

# Match intent from input
def match_intent(user_input: str, intents: list):
    user_input = preprocess(user_input)

    best_match = None
    best_priority = float('inf')

    for intent in intents:
        for pattern in intent.get("patterns", []):
            if re.search(rf'\b{re.escape(pattern.lower())}\b', user_input):
                if intent.get("priority", 999) < best_priority:
                    best_match = intent
                    best_priority = intent.get("priority", 999)

        if not best_match:
            for keyword in intent.get("keywords", []):
                if keyword.lower() in user_input:
                    if intent.get("priority", 999) < best_priority:
                        best_match = intent
                        best_priority = intent.get("priority", 999)

    return best_match

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_bot_response():
    user_input = request.args.get('msg')
    matched_intent = match_intent(user_input, intents)

    if matched_intent:
        return matched_intent["response"]
    else:
        return "I'm sorry, I didn't understand that. Could you rephrase?"

if __name__ == "__main__":
    app.run(debug=True)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # use PORT environment variable
    app.run(host='0.0.0.0', port=port)
