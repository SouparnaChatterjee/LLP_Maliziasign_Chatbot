# test_intent_main.py
import json
import re
from typing import Optional, Dict

def load_intents(filepath: str) -> list:
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data["intents"]

def preprocess(text: str) -> str:
    return text.lower().strip()

def match_intent(user_input: str, intents: list) -> Optional[Dict]:
    user_input = preprocess(user_input)

    best_match = None
    best_priority = float('inf')

    for intent in intents:
        # Direct pattern match
        for pattern in intent.get("patterns", []):
            if re.search(rf'\b{re.escape(pattern.lower())}\b', user_input):
                if intent.get("priority", 999) < best_priority:
                    best_match = intent
                    best_priority = intent.get("priority", 999)
        
        # Fallback: keyword match
        if not best_match:
            for keyword in intent.get("keywords", []):
                if keyword.lower() in user_input:
                    if intent.get("priority", 999) < best_priority:
                        best_match = intent
                        best_priority = intent.get("priority", 999)

    return best_match

# Add this new function for integration
def process_message(user_input: str) -> str:
    try:
        # Load intents from the JSON file
        intents = load_intents("malizia_final_corrected_dataset.json")
        
        # Get matching intent
        matched_intent = match_intent(user_input, intents)
        
        # Return response
        if matched_intent:
            return matched_intent['response']
        else:
            return "I'm sorry, I didn't understand that. Could you rephrase?"
            
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    intents = load_intents("malizia_final_corrected_dataset.json")
    print("Chatbot is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        response = process_message(user_input)
        print(f"Chatbot: {response}")
