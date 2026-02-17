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
# Explicitly separated voice lists
FEMALE_VOICES = ["af_bella", "af_nicole", "af_sky", "bf_emma"]
MALE_VOICES = ["am_adam", "am_michael", "bm_george", "bm_lewis"]

# Combined list for backwards compatibility or fallbacks if needed
VOICE_LIST = FEMALE_VOICES + MALE_VOICES

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
    
    # Create a mapping from speaker name to voice_id ensuring uniqueness
    voice_mapping = {}
    used_voices = set()
    
    for name in unique_speakers:
        gender = speaker_genders.get(name, "Female") if speaker_genders else "Female"
        
        # strict gender selection
        if gender == "Female":
            target_pool = FEMALE_VOICES
            other_pool = MALE_VOICES
        else: # Male
            target_pool = MALE_VOICES
            other_pool = FEMALE_VOICES
        
        # 1. Try unused voice of preferred gender
        voice_id = next((v for v in target_pool if v not in used_voices), None)
        
        # 2. If all preferred gender voices are used, reuse one from preferred gender (Round Robin)
        # We prefer reusing a correct-gendered voice over switching gender
        if not voice_id:
             # Find the least used voice of the correct gender? 
             # For simplicity, just pick one that is already used but correct gender.
             # Or purely random from target_pool. 
             # Let's just pick from target_pool[0] as fallback, or rotate?
             # Let's just pick the first available one to ensure gender correctness.
             if target_pool:
                 voice_id = target_pool[0]
             else:
                 # Should practically never happen unless lists are empty
                 voice_id = VOICE_LIST[0]

        # Note: We deliberately DO NOT fallback to `other_pool` to avoid gender confusion.
                
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



