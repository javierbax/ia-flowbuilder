from fastapi import APIRouter
from services.gancho.models import GanchoInput, GanchoOutput
from pydantic import BaseModel
from typing import List
from core.openai_client import generar_hooks

router = APIRouter()

@router.post("/", response_model=GanchoOutput)
async def generar_gancho(data: GanchoInput):
    resultado = generar_hooks(data.tema, data.formato)
    return resultado

