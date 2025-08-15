# backend/services/llm.py
import google.generativeai as genai
from typing import Dict, List, Any
import config

if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in config.py.")

chat_histories: Dict[str, List[Dict[str, Any]]] = {}

def get_llm_response(session_id: str, user_query: str) -> str:
    if not config.GEMINI_API_KEY:
        raise Exception("Gemini API key not found in config.py.")

    session_history = chat_histories.get(session_id, [])
    model = genai.GenerativeModel('gemini-1.5-flash')

    chat = model.start_chat(history=session_history)
    response = chat.send_message(user_query)
    llm_response_text = response.text

    chat_histories[session_id] = chat.history
    return llm_response_text