# main.py

from fastapi import FastAPI, Form, Request, UploadFile, File, Path
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from dotenv import load_dotenv # --- We are temporarily disabling this for debugging ---
import requests
import os
import assemblyai as aai
import google.generativeai as genai
from typing import Dict, List, Any

# --- We are temporarily disabling this for debugging ---
# load_dotenv() 

app = FastAPI()

# --- Static Files and Templates ---
if not os.path.exists("static"):
    os.makedirs("static")
if not os.path.exists("templates"):
    os.makedirs("templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- API Key Configuration (Temporary Debugging Step) ---
# We are setting the keys directly to bypass the .env file issue.
MURF_API_KEY = "ap2_21a8261f-881b-41eb-8bd8-5b3cf5756f9e"
ASSEMBLYAI_API_KEY = "d9c24a6c121847ba815574820c46d076"
GEMINI_API_KEY = "AIzaSyAA9wa4h8qIhWLHJmlgkaiNmCVS96V0kOI"

# --- Configure API Clients ---
if ASSEMBLYAI_API_KEY:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    print("--- AssemblyAI API Key has been set. ---")
else:
    print("Warning: ASSEMBLYAI_API_KEY not found.")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("--- Gemini API Key has been set. ---")
else:
    print("Warning: GEMINI_API_KEY not found.")

chat_histories: Dict[str, List[Dict[str, Any]]] = {}


@app.get("/")
async def home(request: Request):
    """Serves the main HTML page from the 'templates' directory."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/agent/chat/{session_id}")
async def agent_chat(
    session_id: str = Path(..., description="The unique ID for the chat session."),
    audio_file: UploadFile = File(...)
):
    """
    Handles a full conversational turn with error handling.
    """
    fallback_audio_path = "static/fallback.mp3" 

    if not os.path.exists(fallback_audio_path):
        return JSONResponse(
            status_code=500, 
            content={"error": "Fallback audio file is missing on the server."}
        )

    try:
        # --- Stage 1: Transcribe Audio with AssemblyAI ---
        if not ASSEMBLYAI_API_KEY:
            raise Exception("AssemblyAI API key is not configured.")
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file.file)

        if transcript.status == aai.TranscriptStatus.error or not transcript.text:
             raise Exception(f"Transcription failed: {transcript.error or 'No speech detected'}")

        user_query_text = transcript.text
        print(f"User said: {user_query_text}")
      
        # --- Stage 2: Get a response from the Gemini LLM ---
        if not GEMINI_API_KEY:
            raise Exception("Gemini API key is not configured.")

        session_history = chat_histories.get(session_id, [])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        chat = model.start_chat(history=session_history)
        response = chat.send_message(user_query_text)
        llm_response_text = response.text
        print(f"LLM responded: {llm_response_text}")

        # --- Stage 3: Update the chat history ---
        chat_histories[session_id] = chat.history

        # --- Stage 4: Convert Text-to-Speech with Murf AI ---
        if not MURF_API_KEY:
            raise Exception("Murf AI API key is not configured.")

        print(f"--- Using Murf API Key starting with: {MURF_API_KEY[:5]} ---")

        murf_voice_id = "en-US-natalie" 
        url = "https://api.murf.ai/v1/speech/generate"
        headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        
        payload = {
            "text": llm_response_text,
            "voiceId": murf_voice_id,
            "format": "mp3" 
        }

        murf_response = requests.post(url, json=payload, headers=headers)
        murf_response.raise_for_status() # Raises an HTTPError for bad responses
        response_data = murf_response.json()
        audio_url = response_data.get("audioFile")

        if audio_url:
            return JSONResponse(content={"audio_url": audio_url, "text": llm_response_text})
        else:
            raise Exception("Murf API did not return an audio file.")

    except Exception as e:
        print(f"An error occurred in the agent chat flow: {e}")
        return FileResponse(fallback_audio_path, media_type="audio/mpeg", headers={"X-Error": "true"})
