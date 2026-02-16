import re
import json
from typing import List, Dict, Tuple
from .llm import query_llm

SPEAKERS = [
    {"name": "Alex", "role": "Host", "personality": "curious, enthusiastic, asks clarifying questions, guides the conversation"},
    {"name": "Bailey", "role": "Expert", "personality": "knowledgeable, calm, articulate, explains complex concepts simply"},
    {"name": "Casey", "role": "Skeptic", "personality": "critical thinker, challenges assumptions, looks for evidence, plays devil's advocate"},
    {"name": "Devin", "role": "Futurist", "personality": "energetic, visionary, relates topics to future possibilities and trends"}
]

def get_speaker_config(num_speakers: int, custom_names: List[str] = None) -> List[Dict]:
    """Get the configuration for the requested number of speakers."""
    base_config = SPEAKERS[:max(2, min(num_speakers, 4))]
    
    if custom_names:
        # Override names while keeping roles/personalities
        for i, name in enumerate(custom_names):
            if i < len(base_config) and name.strip():
                base_config[i] = base_config[i].copy() # detailed copy to avoid mutating global
                base_config[i]['name'] = name.strip()
    
    return base_config


def get_speaker_formatting(speakers: List[Dict]) -> Tuple[str, str]:
    """
    Returns the formatted speaker description and JSON format for prompts.
    """
    speakers_desc = "\n".join([f"- {s['name']} ({s['role']}): {s['personality']}" for s in speakers])
    json_format = ",\n    ".join([f'{{"speaker": "{s["name"]}", "text": "..."}}' for s in speakers])
    return speakers_desc, json_format



def count_words(text: str) -> int:
    """Count the number of words in the text."""
    return len(text.split())


def chunk_text(text: str, max_words: int = 500) -> List[str]:
    """
    Split text into chunks of approximately max_words each.
    Respects sentence boundaries to avoid mid-sentence cuts.
    """
    # Split into sentences (simple approach)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        sentence_words = count_words(sentence)
        
        if current_word_count + sentence_words > max_words and current_chunk:
            # Save current chunk and start new one
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_word_count = sentence_words
        else:
            current_chunk.append(sentence)
            current_word_count += sentence_words
    
    # Add the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    print(f"Total chunks created: {len(chunks)}")
    return chunks


def extract_json_from_response(response: str) -> List[Dict]:
    """
    Extract JSON content from LLM response.
    Handles both array format and multiple object format.
    """
    try:
        # First try to find array format []
        start_idx = response.find('[')
        end_idx = response.rfind(']')
        
        if start_idx != -1:
            json_str = response[start_idx:]
            try:
                parsed, _ = json.JSONDecoder().raw_decode(json_str)
                return parsed
            except:
                # If raw_decode fails, fall back to other methods or try finding the last ]
                pass
                
        if start_idx != -1 and end_idx != -1:
            json_str = response[start_idx:end_idx + 1]
            try:
                return json.loads(json_str)
            except:
                pass
        
        # If no array, try to extract multiple JSON objects
        # Look for pattern: {...}\n{...}
        objects = []
        lines = response.strip().split('\n')
        current_obj = ""
        brace_count = 0
        
        for line in lines:
            for char in line:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                current_obj += char
                
                if brace_count == 0 and current_obj.strip():
                    try:
                        obj = json.loads(current_obj.strip())
                        if isinstance(obj, dict) and 'speaker' in obj and 'text' in obj:
                            objects.append(obj)
                        current_obj = ""
                    except:
                        current_obj = ""
        
        if objects:
            return objects
        
        raise ValueError("No valid JSON found in response")
        
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        print(f"Response was: {response[:500]}...")
        return []


def extract_topic_from_chunk(chunk: str, llm_config: dict) -> str:
    """
    Extract a concise topic/theme from a chunk of text using LLM.
    Returns a short topic string (5-10 words).
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that extracts main topics from text."
        },
        {
            "role": "user",
            "content": f"""Read the following text and extract the main topic or theme in 5-10 words.

        Text:
        {chunk}...

        Respond with ONLY the topic, nothing else."""
        }
    ]
    
    try:
        topic = query_llm(
            messages=messages,
            provider=llm_config["provider"],
            model_name=llm_config.get("model_name", ""),
            api_key=llm_config.get("api_key"),
            local_pipeline=llm_config.get("local_pipeline")
        )
        return topic.strip()
    except Exception as e:
        print(f"Error extracting topic: {e}")
        return "General Discussion"


def generate_chunk_dialogue(chunk: str, topic: str, llm_config: dict, speakers: List[Dict]) -> List[Dict]:
    """
    Generate 250-300 word dialogue for a single chunk.
    NO intro, NO outro - just the main content discussion.
    """
    speakers_desc, json_format = get_speaker_formatting(speakers)

    messages = [
        {
            "role": "system",
            "content": f"""You are a podcast script writer. Create engaging dialogue between these hosts:
            {speakers_desc}

            CRITICAL RULES:
            1. Generate 250-300 words of dialogue
            2. DO NOT include any introduction or greeting
            3. DO NOT include any conclusion or sign-off
            4. Jump straight into discussing the topic
            5. Make it conversational and engaging
            6. Output ONLY valid JSON, nothing else"""
        },
        {
            "role": "user",
            "content": f"""Create a 350-500 word dialogue segment about: {topic}

            Based on this content:
            {chunk}

            **Output Format (JSON):**
            [
                {json_format}
            ]

            Remember: NO intro, NO outro. Start directly with the topic discussion. Ensure all speakers participate naturally."""
        }
    ]
    
    try:
        response = query_llm(
            messages=messages,
            provider=llm_config["provider"],
            model_name=llm_config.get("model_name", ""),
            api_key=llm_config.get("api_key"),
            local_pipeline=llm_config.get("local_pipeline")
        )
        dialogue = extract_json_from_response(response)
        print(f"Generated dialogue for topic '{topic}': {dialogue}\n\n")
        return dialogue
    except Exception as e:
        print(f"Error generating chunk dialogue: {e}")
        return []


def stitch_and_refine(chunk_dialogues: List[List[Dict]], llm_config: dict, speakers: List[Dict]) -> List[Dict]:
    """
    Combine all chunk dialogues and rewrite as a cohesive script.
    Maintains natural flow between topics.
    """
    # Flatten all dialogues into one
    combined_dialogue = []
    for dialogue in chunk_dialogues:
        if dialogue:  # Only extend if dialogue is not empty
            combined_dialogue.extend(dialogue)
    
    # If no valid dialogues, return empty
    if not combined_dialogue:
        print("Warning: No valid dialogues to stitch")
        return []
    
    # Convert to readable format for LLM
    dialogue_text = "\n".join([
        f"{turn['speaker']}: {turn['text']}"
        for turn in combined_dialogue
    ])
    
    speakers_desc, json_format = get_speaker_formatting(speakers)

    messages = [
        {
            "role": "system",
            "content": f"""You are a podcast script editor. Rewrite the provided dialogue to make it flow naturally and cohesively.

            CRITICAL RULES:
            1. Maintain the same topics and information
            2. Ensure smooth transitions between topics
            3. Keep the conversational tone between {speakers_desc}
            4. DO NOT add intro or outro
            5. Keep similar length to original
            6. Output ONLY valid JSON"""
        },
        {
            "role": "user",
            "content": f"""Rewrite this dialogue to flow more naturally:

            {dialogue_text}

            **Output Format (JSON):**
            [
                {json_format}
            ]

            Make it cohesive but keep the same content and length."""
        }
    ]
    
    try:
        response = query_llm(
            messages=messages,
            provider=llm_config["provider"],
            model_name=llm_config.get("model_name", ""),
            api_key=llm_config.get("api_key"),
            local_pipeline=llm_config.get("local_pipeline")
        )
        
        refined_dialogue = extract_json_from_response(response)
        print(f"Refined dialogue: {len(refined_dialogue)} turns")
        return refined_dialogue
    except Exception as e:
        print(f"Error refining dialogue: {e}")
        return combined_dialogue


def generate_intro_outro(main_script: List[Dict], llm_config: dict, speakers: List[Dict], podcast_name: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Generate intro and outro based on the final cohesive script.
    Intro: 30-50 words
    Outro: 30-50 words
    """
    # Get overview of main script
    script_preview = "\n".join([
        f"{turn['speaker']}: {turn['text']}"
        for turn in main_script[:5]  # First 5 turns for context
    ])
    
    speakers_desc, json_format = get_speaker_formatting(speakers)

    # Identify the host (assumed to be the first speaker or explicitly searched)
    host_name = next((s['name'] for s in speakers if s['role'] == "Host"), speakers[0]['name'])
    other_speakers = [s['name'] for s in speakers if s['name'] != host_name]
    others_str = ", ".join(other_speakers)

    # Generate intro
    intro_messages = [
        {
            "role": "system",
            "content": f"""You are a podcast script writer. Create a brief, engaging introduction.

            CRITICAL RULES:
            1. 50-75 words
            2. The Host ({host_name}) MUST start by welcoming listeners to "{podcast_name}".
            3. {host_name} MUST introduce themselves and then introduce the other speakers: {others_str}.
            4. Tease the main topics.
            5. Output ONLY valid JSON."""
        },
        {
            "role": "user",
            "content": f"""Create a 50-75 word introduction for this podcast episode:

            Main topics discussed:
            {script_preview}

            **Output Format (JSON):**
            [
                {json_format}
            ]"""
        }
    ]
    
    # Generate outro
    outro_messages = [
        {
            "role": "system",
            "content": f"""You are a podcast script writer. Create a brief, warm conclusion.

            CRITICAL RULES:
            1. 30-50 words only
            2. The Host ({host_name}) MUST summarize key takeaways.
            3. {host_name} MUST thank the other speakers ({others_str}) for joining.
            4. {host_name} signs off the episode.
            5. Output ONLY valid JSON."""
        },
        {
            "role": "user",
            "content": f"""Create a 30-50 word conclusion for this podcast episode:

            Topics covered:
            {script_preview}

            **Output Format (JSON):**
            [
                {json_format}
            ]"""
        }
    ]
    
    try:
        intro_response = query_llm(
            messages=intro_messages,
            provider=llm_config["provider"],
            model_name=llm_config.get("model_name", ""),
            api_key=llm_config.get("api_key"),
            local_pipeline=llm_config.get("local_pipeline")
        )
        intro = extract_json_from_response(intro_response)
        print(f"Generated intro: {intro}")
        
        outro_response = query_llm(
            messages=outro_messages,
            provider=llm_config["provider"],
            model_name=llm_config.get("model_name", ""),
            api_key=llm_config.get("api_key"),
            local_pipeline=llm_config.get("local_pipeline")
        )
        outro = extract_json_from_response(outro_response)
        print(f"Generated outro: {outro}")
        
        return intro, outro
    except Exception as e:
        print(f"Error generating intro/outro: {e}")
        return [], []


def generate_single_call_script(content: str, duration: int, llm_config: dict, speakers: List[Dict]) -> List[Dict]:
    """
    Generate complete script (with intro and outro) in a single LLM call.
    Used for small content (≤ 800 words).
    """
    target_words = duration * 150  # Approximate words per minute
    speakers_desc, json_format = get_speaker_formatting(speakers)

    messages = [
        {
            "role": "system",
            "content": f"""You are a podcast script writer. Create engaging dialogue between these hosts:
{speakers_desc}

Make it conversational, informative, and engaging."""
        },
        {
            "role": "user",
            "content": f"""Create a {duration}-minute podcast script (approximately {target_words} words) based on this content:

{content}

Include:
1. Brief intro (30-50 words)
2. Main discussion
3. Brief outro (30-50 words)

**Output Format (JSON):**
[
    {json_format}
]"""
        }
    ]
    
    try:
        response = query_llm(
            messages=messages,
            provider=llm_config["provider"],
            model_name=llm_config.get("model_name", ""),
            api_key=llm_config.get("api_key"),
            local_pipeline=llm_config.get("local_pipeline")
        )
        
        dialogue = extract_json_from_response(response)
        print(f"Generated single-call script: {len(dialogue)} turns")
        return dialogue
    except Exception as e:
        print(f"Error generating single-call script: {e}")
        return []


def generate_script(content_data: dict, duration: int, llm_config: dict, num_speakers: int = 2, podcast_name: str = "Synth-FM", custom_speaker_names: List[str] = None) -> dict:
    """
    Main orchestrator function for script generation.
    
    Determines whether to use single-call or multi-chunk approach based on word count.
    Returns final script with title and dialogue.
    """
    try:
        content = content_data.get("combined_content", "")
        word_count = count_words(content)
        
        print(f"\n=== Script Generation Started ===")
        print(f"Content word count: {word_count}")
        print(f"Target duration: {duration} minutes")
        
        # Threshold for chunking
        CHUNK_THRESHOLD = 1200
        
        # Get speaker configuration
        speakers = get_speaker_config(num_speakers, custom_speaker_names)
        print(f"Generating script for {num_speakers} speakers: {[s['name'] for s in speakers]}")
        print(f"Podcast Name: {podcast_name}")

        if word_count <= CHUNK_THRESHOLD:
            print("Using single LLM call approach (small content)")
            dialogue = generate_single_call_script(content, duration, llm_config, speakers)
        else:
            print("Using multi-chunk approach (large content)")
            
            # Step 1: Chunk the content
            chunks = chunk_text(content, max_words=3000)
            print(f"Created {len(chunks)} chunks")
            
            # Step 2: Generate dialogue for each chunk
            chunk_dialogues = []
            for i, chunk in enumerate(chunks):
                print(f"\nProcessing chunk {i+1}/{len(chunks)}")
                
                # Extract topic
                topic = extract_topic_from_chunk(chunk, llm_config)
                print(f"Topic: {topic}")
                
                # Generate dialogue
                chunk_dialogue = generate_chunk_dialogue(chunk, topic, llm_config, speakers)
                if chunk_dialogue:
                    chunk_dialogues.append(chunk_dialogue)
            
            # Step 3: Stitch and refine
            print("\nStitching and refining all chunks...")
            main_script = stitch_and_refine(chunk_dialogues, llm_config, speakers)
            
            # Step 4: Generate intro and outro
            print("\nGenerating intro and outro...")
            intro, outro = generate_intro_outro(main_script, llm_config, speakers, podcast_name)
            
            # Step 5: Combine everything
            dialogue = intro + main_script + outro
        
        print(f"\n=== Script Generation Complete ===")
        print(f"Total dialogue turns: {len(dialogue)}")
        
        return {
            "title": f"{podcast_name} Podcast",
            "dialogue": dialogue
        }
        
    except Exception as e:
        print(f"Error in generate_script: {e}")
        return {
            "error": f"Script generation failed: {str(e)}"
        }
