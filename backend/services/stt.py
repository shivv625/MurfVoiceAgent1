# backend/services/stt.py
import assemblyai as aai
from fastapi import UploadFile
import config

if config.ASSEMBLYAI_API_KEY:
    aai.settings.api_key = config.ASSEMBLYAI_API_KEY
else:
    print("Warning: ASSEMBLYAI_API_KEY not found in config.py.")

def transcribe_audio(audio_file: UploadFile) -> str:
    if not config.ASSEMBLYAI_API_KEY:
        raise Exception("AssemblyAI API key not found in config.py.")

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file.file)

    if transcript.status == aai.TranscriptStatus.error or not transcript.text:
        raise Exception(f"Transcription failed: {transcript.error or 'No speech detected'}")

    return transcript.text