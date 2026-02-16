from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.utils.llm import get_local_model_pipeline, unload_local_model, MODEL_LOCAL_3B, MODEL_LOCAL_1B

MODEL_MAPPING = {
    "local_3b": MODEL_LOCAL_3B,
    "local_1b": MODEL_LOCAL_1B
}

router = APIRouter()

class LoadModelRequest(BaseModel):
    model_name: str

@router.post("/load")
async def load_model(request: LoadModelRequest):
    try:
        mapped_name = MODEL_MAPPING.get(request.model_name, request.model_name)
        pipe = get_local_model_pipeline(mapped_name)
        if pipe:
            return {"status": "success", "message": f"Model {request.model_name} loaded successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to load model")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/unload")
async def unload_model():
    try:
        result = unload_local_model()
        return {"status": "success", "message": "Model unloaded", "nvidia_smi": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
