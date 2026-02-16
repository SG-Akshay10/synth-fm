from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.schemas import AudioRequest, AudioResponse, FinalAudioRequest, FinalAudioResponse, ScriptResponse
from backend.utils.audio_synthesizer import batch_synthesize_audio
from backend.utils.audio_processor import create_podcast
from backend.utils.llm import unload_local_model
import os

router = APIRouter()

@router.post("/synthesize-audio", response_model=AudioResponse)
async def synthesize_audio_segments(request: AudioRequest):
    # Unload local LLM if needed to free VRAM for TTS
    # In a real deployed scenario, LLM and TTS might be on different services or queues.
    # For this local setup, we unload.
    if request.provider == "local":
        unload_local_model()

    try:
        # Reconstruct script dict from model
        script_dict = request.script.dict()
        
        audio_paths = batch_synthesize_audio(
            script=script_dict,
            unique_speakers=request.speaker_names,
            speaker_genders=request.speaker_genders
        )
        
        return {"audio_paths": audio_paths}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-podcast", response_model=FinalAudioResponse)
async def create_final_podcast(request: FinalAudioRequest):
    try:
        final_path = create_podcast(request.audio_paths)
        return {"final_audio_path": final_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-podcast")
async def download_podcast(path: str):
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/wav", filename="podcast.wav")
    raise HTTPException(status_code=404, detail="File not found")
