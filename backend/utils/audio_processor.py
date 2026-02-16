import numpy as np
import soundfile as sf
from pathlib import Path

OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_podcast(audio_segments: list[str], output_filename: str = "final_podcast.wav") -> str:
    """
    Stitches audio segments using numpy and soundfile.
    """
    if not audio_segments:
        return None
        
    all_audio = []
    sample_rate = 24000 # Default for Kokoro
    
    for segment_path in audio_segments:
        try:
            data, sr = sf.read(segment_path)
            all_audio.append(data)
            sample_rate = sr # Keep the last one, assuming all same
        except Exception as e:
            print(f"Error processing segment {segment_path}: {e}")
            
    if not all_audio:
        return None
        
    # Concatenate all segments
    combined = np.concatenate(all_audio)
    
    # Ensure output_filename ends with .wav for consistency with our new implementation
    if not output_filename.endswith(".wav"):
        output_filename = output_filename.rsplit(".", 1)[0] + ".wav"
        
    output_path = OUTPUT_DIR / output_filename
    
    # Export as WAV
    try:
        sf.write(str(output_path), combined, sample_rate)
        return str(output_path)
    except Exception as e:
        print(f"Error exporting podcast: {e}")
        return None

