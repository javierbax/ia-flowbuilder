import os
import uuid
from fastapi import UploadFile
from core.whisper_client import transcribe_audio
from core.client import client
from services.audio.models import AudioToIdeasOutput
from core.supabase_client import supabase
import time
from langdetect import detect

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"


def summarize_text(text: str, lang_code: str = "en") -> tuple[str, dict]:
    if lang_code == "es":
        prompt = f"""
Eres un asistente que resume audios para creadores de contenido en español.

Aquí está la transcripción:
{text}

Genera un resumen en viñetas, conciso, en español.
"""
    else:
        prompt = f"""
You are an assistant that summarizes voice notes for content creators.

Here is the transcript:
{text}

Generate a concise bullet-point summary in English.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=300
    )
    summary = response.choices[0].message.content.strip()
    usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else response.usage
    return summary, usage



def process_audio_file(file: UploadFile) -> AudioToIdeasOutput:
    start = time.time()
    temp_dir = "tmp"
    os.makedirs(temp_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(temp_dir, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    transcript = transcribe_audio(file_path)
    lang = detect_language(transcript)
    summary, usage = summarize_text(transcript, lang)
    duration = int((time.time() - start) * 1000)  # ms

    # Save usage to Supabase
    supabase.table("usage_logs").insert({
        "microservice": "audio-to-ideas",
        "prompt_tokens": usage["prompt_tokens"],
        "completion_tokens": usage["completion_tokens"],
        "total_tokens": usage["total_tokens"],
        "duration_ms": duration
    }).execute()

    return AudioToIdeasOutput(transcript=transcript, summary=summary, language=lang)

