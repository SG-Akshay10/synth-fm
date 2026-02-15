import os
import asyncio
import edge_tts
from pathlib import Path

# Voice Mapping for Edge TTS
VOICE_PROFILES = {
    "Alex": "en-US-AvaNeural",      # Enthusiastic female
    "Bailey": "en-US-AndrewNeural", # Analytical male
    "Casey": "en-US-EmmaNeural",    # Expert female
    "Drew": "en-US-BrianNeural"     # Deep voice male
}

TEMP_DIR = Path("data/temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

async def synthesize_segment_async(segment_index: int, speaker: str, text: str) -> str:
    """Async synthesis a single audio segment using Edge TTS."""
    voice = VOICE_PROFILES.get(speaker, "en-US-AvaNeural")
    file_path = TEMP_DIR / f"segment_{segment_index}_{speaker}.mp3"
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(file_path))
        return str(file_path)
    except Exception as e:
        print(f"Error synthesizing segment {segment_index}: {e}")
        return None

async def batch_synthesize_async(script: dict) -> list[str]:
    """Process all dialogue segments concurrently."""
    dialogue = script.get("dialogue", [])
    tasks = []
    
    for i, turn in enumerate(dialogue):
        tasks.append(
            synthesize_segment_async(i, turn.get("speaker"), turn.get("text"))
        )
        
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]

def batch_synthesize_audio(script: dict) -> list[str]:
    """Wrapper to run async synthesis from sync context."""
    return asyncio.run(batch_synthesize_async(script))

