from fastapi import APIRouter
from services.voz.models import VozInput, VozOutput
from services.voz.service import procesar_voz

router = APIRouter()

@router.post("/", response_model=VozOutput)
def generar_audio(data: VozInput):
    return procesar_voz(data.texto_principal, data.voice_id)
