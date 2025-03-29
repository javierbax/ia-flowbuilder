from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Input(BaseModel):
    input: str

@router.post("/")
def process(data: Input):
    return {{"result": f"Procesado: {{data.input}}"}}