from pydantic import BaseModel
from typing import Optional

class AudioToIdeasInput(BaseModel):
    filename: str  # path to uploaded file (you can later replace this with UploadFile)

class AudioToIdeasOutput(BaseModel):
    transcript: str
    summary: str
    language: str


