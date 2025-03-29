from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from services.audio.service import process_audio_file
from services.audio.models import AudioToIdeasOutput

router = APIRouter()

@router.post("/", response_model=AudioToIdeasOutput)
async def audio_to_ideas(file: UploadFile = File(...)):
    try:
        result = process_audio_file(file)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
