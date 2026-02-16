import os
import numpy as np
import soundfile as sf
from kokoro import KPipeline
import torch
from pathlib import Path

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

# Default voices for dynamic mapping (Expanded for variety)
VOICE_LIST = [
    "af_bella", "af_nicole", "af_sky", "bf_emma",  # Female voices
    "am_adam", "am_michael", "bm_george", "bm_lewis"  # Male voices
]

def synthesize_segment_kokoro(segment_index: int, speaker: str, text: str, voice_id: str) -> str:
    """Synthesize a single audio segment using Kokoro TTS (Sync)."""
    try:
        pipeline = get_kokoro_pipeline()
        
        # Kokoro returns a generator
        generator = pipeline(text, voice=voice_id, speed=1)
        
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

def batch_synthesize_audio(script: dict, unique_speakers: list[str], speaker_genders: dict[str, str] = None) -> list[str]:
    """Process all dialogue segments sequentially for Kokoro."""
    dialogue = script.get("dialogue", [])
    results = []
    
    # Categorize voices
    female_voices = [v for v in VOICE_LIST if v.startswith("af_")]
    male_voices = [v for v in VOICE_LIST if v.startswith("am_")]
    
    # Create a mapping from speaker name to voice_id ensuring uniqueness
    voice_mapping = {}
    used_voices = set()
    
    for name in unique_speakers:
        gender = speaker_genders.get(name, "Female") if speaker_genders else "Female"
        
        target_pool = female_voices if gender == "Female" else male_voices
        other_pool = male_voices if gender == "Female" else female_voices
        
        # 1. Try unused voice of preferred gender
        voice_id = next((v for v in target_pool if v not in used_voices), None)
        
        # 2. Fallback to unused voice of other gender
        if not voice_id:
            voice_id = next((v for v in other_pool if v not in used_voices), None)
            
        # 3. Last fallback (reuse): pick a voice of preferred gender (if pool not empty)
        if not voice_id:
            if target_pool:
                voice_id = target_pool[0]  # Just pick the first one of preferred gender
            else:
                voice_id = VOICE_LIST[0]   # Global fallback
                
        voice_mapping[name] = voice_id
        used_voices.add(voice_id)
    
    for i, turn in enumerate(dialogue):
        speaker = turn.get("speaker")
        text = turn.get("text")
        voice_id = voice_mapping.get(speaker, VOICE_LIST[0])
        
        path = synthesize_segment_kokoro(i, speaker, text, voice_id)
        if path:
            results.append(path)
            
    return results



