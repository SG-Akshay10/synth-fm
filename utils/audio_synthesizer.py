import os
import asyncio
import edge_tts
import soundfile as sf
from kokoro import KPipeline
import torch
from pathlib import Path

# Voice Mapping for Edge TTS
VOICE_PROFILES = {
    "Alex": "en-US-AvaNeural",      # Enthusiastic female
    "Bailey": "en-US-AndrewNeural", # Analytical male
    "Casey": "en-US-EmmaNeural",    # Expert female
    "Drew": "en-US-BrianNeural"     # Deep voice male
}

# Voice Mapping for Kokoro
KOKORO_VOICES = {
    "Alex": "af_heart",     # Example mapping
    "Bailey": "am_adam",    # Example mapping
    "Casey": "af_bella",    # Example mapping
    "Drew": "am_michael"    # Example mapping
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

async def synthesize_segment_edge(segment_index: int, speaker: str, text: str) -> str:
    """Async synthesis a single audio segment using Edge TTS."""
    voice = VOICE_PROFILES.get(speaker, "en-US-AvaNeural")
    file_path = TEMP_DIR / f"segment_{segment_index}_{speaker}.mp3"
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(file_path))
        return str(file_path)
    except Exception as e:
        print(f"Error synthesizing segment {segment_index} (Edge): {e}")
        return None

def synthesize_segment_kokoro(segment_index: int, speaker: str, text: str) -> str:
    """Synthesize a single audio segment using Kokoro TTS (Sync)."""
    try:
        pipeline = get_kokoro_pipeline()
        voice = KOKORO_VOICES.get(speaker, "af_heart")
        
        # Kokoro returns a generator
        generator = pipeline(text, voice=voice, speed=1)
        
        # We need to concatenate all audio chunks if there are multiple sentences
        # but for short segments usually one check. 
        # However pipeline(text) yields (graphemes, phonemes, audio)
        
        all_audio = []
        for _, _, audio in generator:
            all_audio.append(audio)
            
        if not all_audio:
            return None
            
        import numpy as np
        final_audio = np.concatenate(all_audio)
        
        file_path = TEMP_DIR / f"segment_{segment_index}_{speaker}.wav"
        
        # Save as WAV (24khz is default for Kokoro)
        sf.write(str(file_path), final_audio, 24000)
        return str(file_path)
        
    except Exception as e:
        print(f"Error synthesizing segment {segment_index} (Kokoro): {e}")
        return None

async def synthesize_segment_router(segment_index: int, speaker: str, text: str, model: str) -> str:
    if model == "kokoro":
        # Run sync function in thread execution
        return await asyncio.to_thread(synthesize_segment_kokoro, segment_index, speaker, text)
    else:
        return await synthesize_segment_edge(segment_index, speaker, text)

async def batch_synthesize_async(script: dict, model: str = "edge") -> list[str]:
    """Process all dialogue segments concurrently."""
    dialogue = script.get("dialogue", [])
    tasks = []
    
    for i, turn in enumerate(dialogue):
        tasks.append(
            synthesize_segment_router(i, turn.get("speaker"), turn.get("text"), model)
        )
        
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]

def batch_synthesize_audio(script: dict, model: str = "edge") -> list[str]:
    """Wrapper to run async synthesis from sync context."""
    return asyncio.run(batch_synthesize_async(script, model))


