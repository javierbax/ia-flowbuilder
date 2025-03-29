import uuid
import os
from services.voz.models import VozOutput
from core.elevenlabs_client import generate_audio  # asume que ya tienes esto

AUDIO_DIR = "static/audio"

def procesar_voz(texto: str, voice_id: str) -> VozOutput:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.mp3"
    file_path = os.path.join(AUDIO_DIR, filename)

    audio_bytes = generate_audio(texto, voice_id)  # ← aquí pasa el voice_id dinámico

    with open(file_path, "wb") as f:
        f.write(audio_bytes)

    audio_url = f"/static/audio/{filename}"
    return VozOutput(audio_url=audio_url)
