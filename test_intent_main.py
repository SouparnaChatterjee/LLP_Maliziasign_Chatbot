import json
import re
from typing import Optional, Dict

# loads the json file
def load_intents(filepath: str) -> list:
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data["intents"]

# to keep the text free of punctuations, capitals and unnecessary spaces
def preprocess(text: str) -> str:
    return text.lower().strip()


def match_intent(user_input: str, intents: list) -> list:
    # usr_input = preprocess(user_input)
    usr_input = user_input.lower().strip()

    responses = []

    for intent in intents:
        matched = False

        # Pattern match
        for pattern in intent.get("patterns", []):
            if re.search(rf'\b{re.escape(pattern.lower())}\b', usr_input):
                matched = True
                break

        # Keyword match (only if pattern didn't match)
        if not matched:
            for keyword in intent.get("keywords", []):
                if keyword.lower() in usr_input:
                    matched = True
                    break

        # Collect responses if matched
        if matched:
            responses.append(intent["response"])
    
    return responses


# to match the user input with the intents to get the required answers

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

if __name__ == "__main__":
    # Load intents from the JSON file
    intents = load_intents("malizia_final_corrected_dataset.json")

    print("Chatbot is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        matched_intent = match_intent(user_input, intents)

        if matched_intent:
            print(f"Chatbot: {matched_intent['response']}")
        else:
            print("Chatbot: I'm sorry, I didn't understand that. Could you rephrase?")


def process_message(user_input: str) -> str:
    # Load intents
    intents = load_intents("malizia_final_corrected_dataset.json")
    
    # Get matching intent
    matched_intent = match_intent(user_input, intents)
    
    # Return response
    if matched_intent:
        return matched_intent['response']
    else:
        return "I'm sorry, I didn't understand that. Could you rephrase?"

