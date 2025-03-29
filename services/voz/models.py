from pydantic import BaseModel

class VozInput(BaseModel):
    texto_principal: str
    idioma: str = "es"
    voice_id: str


class VozOutput(BaseModel):
    audio_url: str
