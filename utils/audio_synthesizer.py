import os
import numpy as np
import soundfile as sf
from kokoro import KPipeline
import torch
from pathlib import Path

# Voice Mapping for Kokoro
KOKORO_VOICES = {
    "Alex": "af_heart",
    "Bailey": "am_adam",
    "Casey": "af_bella",
    "Drew": "am_michael"
}

TEMP_DIR = Path("data/temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Global pipeline cache to avoid reloading
_KOKORO_PIPELINE = None

def get_kokoro_pipeline():
    global _KOKORO_PIPELINE
    if _KOKORO_PIPELINE is None:
        # lang_code='a' is for American English
        _KOKORO_PIPELINE = KPipeline(lang_code='a')
    return _KOKORO_PIPELINE

def synthesize_segment_kokoro(segment_index: int, speaker: str, text: str) -> str:
    """Synthesize a single audio segment using Kokoro TTS (Sync)."""
    try:
        pipeline = get_kokoro_pipeline()
        voice = KOKORO_VOICES.get(speaker, "af_heart")
        
        # Kokoro returns a generator
        generator = pipeline(text, voice=voice, speed=1)
        
        all_audio = []
        for _, _, audio in generator:
            if audio is not None:
                all_audio.append(audio)
            
        if not all_audio:
            return None
            
        final_audio = np.concatenate(all_audio)
        
        file_path = TEMP_DIR / f"segment_{segment_index}_{speaker}.wav"
        
        # Save as WAV (24khz is default for Kokoro)
        sf.write(str(file_path), final_audio, 24000)
        return str(file_path)
        
    except Exception as e:
        print(f"Error synthesizing segment {segment_index} (Kokoro): {e}")
        return None

def batch_synthesize_audio(script: dict, model: str = "kokoro") -> list[str]:
    """Process all dialogue segments sequentially for Kokoro."""
    dialogue = script.get("dialogue", [])
    results = []
    
    for i, turn in enumerate(dialogue):
        path = synthesize_segment_kokoro(i, turn.get("speaker"), turn.get("text"))
        if path:
            results.append(path)
            
    return results



