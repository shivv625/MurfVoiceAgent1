# backend/services/tts.py
import requests
import config

def convert_text_to_speech(text: str) -> str:
    if not config.MURF_API_KEY:
        raise Exception("Murf AI API key not found in config.py.")

    murf_voice_id = "en-US-natalie"
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {"Content-Type": "application/json", "api-key": config.MURF_API_KEY}

    payload = {
        "text": text,
        "voiceId": murf_voice_id,
        "format": "mp3"
    }

    murf_response = requests.post(url, json=payload, headers=headers)
    murf_response.raise_for_status()
    response_data = murf_response.json()
    audio_url = response_data.get("audioFile")

    if not audio_url:
        raise Exception("Murf API did not return an audio file.")

    return audio_url