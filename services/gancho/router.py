from fastapi import APIRouter
from .schemas import GanchoInput, GanchoOutput
from .service import generar_gancho

router = APIRouter(prefix="/gancho")

@router.post("/", response_model=GanchoOutput)
def handler(data: GanchoInput):
    return generar_gancho(data)
