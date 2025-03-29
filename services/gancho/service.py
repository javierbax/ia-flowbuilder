from .schemas import GanchoInput, GanchoOutput
from core.openai_client import completar_openai

def generar_gancho(data: GanchoInput) -> GanchoOutput:
    prompt = f"Genera un gancho viral con tono {data.tono} sobre: {data.texto}"
    resultado = completar_openai(prompt)
    return GanchoOutput(output=resultado)
