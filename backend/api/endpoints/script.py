from fastapi import APIRouter, HTTPException
from backend.schemas import ScriptRequest, ScriptResponse, ScriptResponse
from backend.utils.script_generator import generate_script
from backend.utils.llm import PROVIDER_OPENAI, PROVIDER_GEMINI, PROVIDER_LOCAL, PROVIDER_GROQ, MODEL_GROQ_LLAMA_3_1_8B_INSTANT, MODEL_GEMINI_FLASH, GEMINI_MODELS
import os

PROVIDER_MAPPING = {
    "openai": PROVIDER_OPENAI,
    "gemini": PROVIDER_GEMINI,
    "local": PROVIDER_LOCAL,
    "groq": PROVIDER_GROQ
}

router = APIRouter()

@router.post("/generate-script", response_model=ScriptResponse)
async def generate_podcast_script(request: ScriptRequest):
    content = {
        "combined_content": request.content,
        "total_word_count": len(request.content.split()), # approximate count
        "valid": True
    }
    
    provider = PROVIDER_MAPPING.get(request.provider, request.provider)
    model_name = request.model_name

    # Sanitize model name for Groq if it receives a local model name
    if provider == PROVIDER_GROQ:
        if not model_name or "local" in model_name.lower() or model_name == "undefined":
            print(f"Sanitizing Groq model name: replaced '{model_name}' with '{MODEL_GROQ_LLAMA_3_1_8B_INSTANT}'")
            model_name = MODEL_GROQ_LLAMA_3_1_8B_INSTANT

    # Sanitize model name for Gemini if it receives a local model name or invalid model
    if provider == PROVIDER_GEMINI:
         if model_name not in GEMINI_MODELS:
            print(f"Sanitizing Gemini model name: replaced '{model_name}' with '{MODEL_GEMINI_FLASH}' (Valid models: {GEMINI_MODELS})")
            model_name = MODEL_GEMINI_FLASH

    llm_config = {
        "provider": provider,
        "api_key": request.api_key,
        "model_name": model_name
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
