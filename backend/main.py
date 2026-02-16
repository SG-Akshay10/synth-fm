

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.api.endpoints import content, script, audio, model

load_dotenv()

app = FastAPI(title="Synth-FM API", version="1.0.0")

# CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(script.router, prefix="/api/script", tags=["script"])
app.include_router(audio.router, prefix="/api/audio", tags=["audio"])
app.include_router(model.router, prefix="/api/model", tags=["model"])

@app.get("/")
async def root():
    return {"message": "Synth-FM Backend is running"}
