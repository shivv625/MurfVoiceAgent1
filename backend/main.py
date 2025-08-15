# backend/main.py
import logging
import os
from fastapi import FastAPI, Request, UploadFile, File, Path
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from services.stt import transcribe_audio
from services.llm import get_llm_response
from services.tts import convert_text_to_speech

# --- App Setup ---
app = FastAPI()

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Static Files and Templates ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# --- Pydantic Schemas ---
class ChatResponse(BaseModel):
    audio_url: str
    text: str


# --- Routes ---
@app.get("/")
async def home(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/agent/chat/{session_id}", response_model=ChatResponse)
async def agent_chat(
    session_id: str = Path(..., description="The unique ID for the chat session."),
    audio_file: UploadFile = File(...)
):
    """Handles a full conversational turn."""
    fallback_audio_path = "static/fallback.mp3"

    try:
        # --- Stage 1: Transcribe Audio ---
        logger.info(f"[{session_id}] Transcribing audio...")
        user_query_text = transcribe_audio(audio_file)
        logger.info(f"[{session_id}] User said: {user_query_text}")

        # --- Stage 2: Get LLM Response ---
        logger.info(f"[{session_id}] Getting LLM response...")
        llm_response_text = get_llm_response(session_id, user_query_text)
        logger.info(f"[{session_id}] LLM responded: {llm_response_text}")

        # --- Stage 3: Convert Text to Speech ---
        logger.info(f"[{session_id}] Converting text to speech...")
        audio_url = convert_text_to_speech(llm_response_text)

        return ChatResponse(audio_url=audio_url, text=llm_response_text)

    except Exception as e:
        logger.error(f"[{session_id}] An error occurred: {e}")
        return FileResponse(
            fallback_audio_path,
            media_type="audio/mpeg",
            headers={"X-Error": "true"}
        )