from pydub import AudioSegment
from pathlib import Path

OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_podcast(audio_segments: list[str], output_filename: str = "final_podcast.mp3") -> str:
    """
    Stitches audio segments with crossfades and normalization.
    """
    if not audio_segments:
        return None
        
    combined = AudioSegment.empty()
    
    # 50ms silence between segments if crossfade isn't possible, or just append
    # But we want crossfade
    crossfade_duration = 100 # ms
    
    for i, segment_path in enumerate(audio_segments):
        try:
            segment = AudioSegment.from_file(segment_path)
            
            if i == 0:
                combined += segment
            else:
                # Append with crossfade
                combined = combined.append(segment, crossfade=crossfade_duration)
        except Exception as e:
            print(f"Error processing segment {segment_path}: {e}")
            
    # Normalize
    # Simple peak normalization
    combined = combined.normalize()
    
    output_path = OUTPUT_DIR / output_filename
    
    # Export
    try:
        combined.export(output_path, format="mp3", bitrate="192k")
        return str(output_path)
    except Exception as e:
        print(f"Error exporting podcast: {e}")
        return None
