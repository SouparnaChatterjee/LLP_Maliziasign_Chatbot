# AI project/chatbot_processor.py
# chatbot_processor.py
from test_intent_main import process_message

def get_chatbot_response(message):
    try:
        response = process_message(message)
        return response
    except Exception as e:
        return f"Error processing message: {str(e)}"
