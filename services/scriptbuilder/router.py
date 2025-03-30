from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
import openai

router = APIRouter()

# --- Models ---
class ScriptRequest(BaseModel):
    topic: str
    duration: Literal[30, 60] = 30  # seconds

class ScriptResponse(BaseModel):
    hook: str
    body: str
    cta: str

# --- Utils ---
def build_prompt(topic: str, duration: int) -> str:
    word_range = "70–90" if duration == 30 else "120–150"
    return (
        f"Escribe un hook llamativo, seguido de 2–3 frases breves que desarrollen el tema. "
        f"Finaliza con un llamado a la acción. Tema: '{topic}'. "
        f"Debe tener entre {word_range} palabras. Devuelve cada parte como: 'Hook:', 'Cuerpo:', 'CTA:'"
    )

# --- Endpoint ---
@router.post("/scriptbuilder", response_model=ScriptResponse)
async def generate_script(data: ScriptRequest):
    prompt = build_prompt(data.topic, data.duration)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message["content"]

        # Simple parsing (assumes consistent format)
        lines = content.split("\n")
        hook = next((l.replace("Hook:", "").strip() for l in lines if l.startswith("Hook:")), "")
        body = next((l.replace("Cuerpo:", "").strip() for l in lines if l.startswith("Cuerpo:")), "")
        cta = next((l.replace("CTA:", "").strip() for l in lines if l.startswith("CTA:")), "")

        return ScriptResponse(hook=hook, body=body, cta=cta)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
