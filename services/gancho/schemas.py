from pydantic import BaseModel

class GanchoInput(BaseModel):
    texto: str
    tono: str = "emocional"

class GanchoOutput(BaseModel):
    output: str
