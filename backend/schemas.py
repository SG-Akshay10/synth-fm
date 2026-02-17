from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class URLRequest(BaseModel):
    urls: List[str]

class ContentResponse(BaseModel):
    combined_content: str
    total_word_count: int
    sources_summary: List[str]
    valid: bool
    error: Optional[str] = None

class ScriptRequest(BaseModel):
    content: str
    duration: int
    num_speakers: int
    podcast_name: str
    speaker_names: List[str]
    provider: str
    api_key: Optional[str] = None
    model_name: str
    tone: Optional[str] = "Fun & Engaging"
    custom_instructions: Optional[str] = None

class DialogueTurn(BaseModel):
    speaker: str
    text: str

class ScriptResponse(BaseModel):
    title: str
    dialogue: List[DialogueTurn]
    error: Optional[str] = None

class AudioRequest(BaseModel):
    script: ScriptResponse
    speaker_names: List[str]
    speaker_genders: Dict[str, str]
    provider: str # "local" or others for now
    model_name: Optional[str] = None

class AudioResponse(BaseModel):
    audio_paths: List[str]
    
class FinalAudioRequest(BaseModel):
    audio_paths: List[str]

class FinalAudioResponse(BaseModel):
    final_audio_path: str
