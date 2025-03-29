# core/image_client.py
from core.client import client

def generar_imagen(descripcion: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=descripcion,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response.data[0].url
