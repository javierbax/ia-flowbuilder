from fastapi import FastAPI
from services.gancho.router import router as gancho_router
from services.post.router import router as post_router
from services.audio.router import router as audio_router
from services.voz.router import router as voz_router
from services.visualizer.router import router as visualizer_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(gancho_router, prefix="/gancho", tags=["GanchoExpress"])
app.include_router(post_router, prefix="/post", tags=["PostMultiplicador"])
app.include_router(audio_router, prefix="/audio", tags=["AudioToIdeas"])
app.include_router(voz_router, prefix="/voz", tags=["VozPremium"])
app.include_router(visualizer_router, prefix="/visualizer", tags=["VisualizerIA"])
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "online"}