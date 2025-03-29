from pydantic import BaseModel
from typing import List

class GanchoInput(BaseModel):
    tema: str
    formato: str

class GanchoOutput(BaseModel):
    hooks: List[str]
    titulo: str
    caption: str
    asunto_email: str
