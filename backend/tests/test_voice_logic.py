
import sys
import os
from unittest.mock import MagicMock, patch

# Mock dependencies that might not be present or needed for logic testing
sys.modules["soundfile"] = MagicMock()
sys.modules["kokoro"] = MagicMock()
sys.modules["numpy"] = MagicMock()
sys.modules["torch"] = MagicMock()

# Add backend/utils to sys.path to import directly without package init overhead
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))

import audio_synthesizer

def test_voice_assignment():
    print("Testing Voice Assignment Logic...")
    
    # Mock the synthesizer to avoid actual audio generation and tracking calls
    with patch('utils.audio_synthesizer.synthesize_segment_kokoro') as mock_synthesize:
        mock_synthesize.return_value = "/tmp/dummy.wav"
        
        # Test Case 1: Single Female
        script = {"dialogue": [{"speaker": "Alice", "text": "Hello"}]}
        speakers = ["Alice"]
        genders = {"Alice": "Female"}
        
        audio_synthesizer.batch_synthesize_audio(script, speakers, genders)
        
        # Check explicit call args
        args, _ = mock_synthesize.call_args
        # args: (segment_index, speaker, text, voice_id)
        voice_id = args[3]
        print(f"Case 1 (Female): Assigned {voice_id}")
        assert voice_id in audio_synthesizer.FEMALE_VOICES, f"Expected female voice, got {voice_id}"
        assert voice_id not in audio_synthesizer.MALE_VOICES

        # Test Case 2: Single Male
        script = {"dialogue": [{"speaker": "Bob", "text": "Hello"}]}
        speakers = ["Bob"]
        genders = {"Bob": "Male"}
        
        audio_synthesizer.batch_synthesize_audio(script, speakers, genders)
        
        args, _ = mock_synthesize.call_args
        voice_id = args[3]
        print(f"Case 2 (Male): Assigned {voice_id}")
        assert voice_id in audio_synthesizer.MALE_VOICES, f"Expected male voice, got {voice_id}"

        # Test Case 3: Mixed
        script = {"dialogue": [
            {"speaker": "Alice", "text": "Hi"},
            {"speaker": "Bob", "text": "Yo"}
        ]}
        speakers = ["Alice", "Bob"]
        genders = {"Alice": "Female", "Bob": "Male"}
        
        # We need to capture multiple calls. 
        # But batch_synthesize_audio might run sequentially. 
        # mock_synthesize will retain history.
        mock_synthesize.reset_mock()
        
        audio_synthesizer.batch_synthesize_audio(script, speakers, genders)
        
        assert mock_synthesize.call_count == 2
        
        calls = mock_synthesize.call_args_list
        # Call 1 -> Alice
        args1, _ = calls[0]
        voice1 = args1[3]
        assert voice1 in audio_synthesizer.FEMALE_VOICES
        
        # Call 2 -> Bob
        args2, _ = calls[1]
        voice2 = args2[3]
        assert voice2 in audio_synthesizer.MALE_VOICES
        
        print(f"Case 3 (Mixed): Alice->{voice1}, Bob->{voice2} - PASSED")

        # Test Case 4: Overflow (More speakers than voices)
        # 5 females (only 4 voices available)
        females = ["F1", "F2", "F3", "F4", "F5"]
        script = {"dialogue": [{"speaker": f, "text": "."} for f in females]}
        genders = {f: "Female" for f in females}
        
        mock_synthesize.reset_mock()
        audio_synthesizer.batch_synthesize_audio(script, females, genders)
        
        assigned_voices = [call[0][3] for call in mock_synthesize.call_args_list]
        print(f"Case 4 (Overflow): {assigned_voices}")
        
        for v in assigned_voices:
            assert v in audio_synthesizer.FEMALE_VOICES
            
        assert len(set(assigned_voices)) == 4 # Should have used all 4 unique voices
        
    print("\nALL TESTS PASSED!")

if __name__ == "__main__":
    test_voice_assignment()
