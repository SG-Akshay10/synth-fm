from fastapi import APIRouter, HTTPException
from backend.schemas import ScriptRequest, ScriptResponse, ScriptResponse
from backend.utils.script_generator import generate_script
from backend.utils.llm import PROVIDER_OPENAI, PROVIDER_GEMINI, PROVIDER_LOCAL
import os

PROVIDER_MAPPING = {
    "openai": PROVIDER_OPENAI,
    "gemini": PROVIDER_GEMINI,
    "local": PROVIDER_LOCAL
}

router = APIRouter()

@router.post("/generate-script", response_model=ScriptResponse)
async def generate_podcast_script(request: ScriptRequest):
    content = {
        "combined_content": request.content,
        "total_word_count": len(request.content.split()), # approximate count
        "valid": True
    }
    
    llm_config = {
        "provider": PROVIDER_MAPPING.get(request.provider, request.provider),
        "api_key": request.api_key,
        "model_name": request.model_name
    }
    
    # If local provider is used, we need to handle loading the pipeline or ensure it's loaded.
    # The original app loaded it into session_state. 
    # For a stateless API, we might need a global model manager or load on demand (slow).
    # Ideally, we should have a Singleton model loader for the local model.
    
    if request.provider == "local":
        # Placeholder for local model loading strategy
        # For now, we assume the environment is set up or we implement get_local_model_pipeline here
        from backend.utils.llm import get_local_model_pipeline
        # This might be slow if loaded every request. 
        # In production, we'd load this at startup or keep it in memory.
        pass

    try:
        script = generate_script(
            content_data=content,
            duration=request.duration,
            llm_config=llm_config,
            num_speakers=request.num_speakers,
            podcast_name=request.podcast_name,
            custom_speaker_names=request.speaker_names
        )
        
        if "error" in script:
            raise HTTPException(status_code=500, detail=script["error"])
            
        return script
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
