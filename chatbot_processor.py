# AI project/chatbot_processor.py

from test_intent_main import process_message  # your existing processing function

def get_chatbot_response(message):
    try:
        response = process_message(message)
        return response
    except Exception as e:
        return str(e)
