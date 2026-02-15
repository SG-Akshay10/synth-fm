import json
import streamlit as st
from utils.llm import query_llm, PROVIDER_OPENAI, PROVIDER_GEMINI, PROVIDER_LOCAL

PERSONAS = {
    "host_a": {"name": "Alex", "style": "enthusiastic, curious, asks clarifying questions", "role": "Host"},
    "host_b": {"name": "Bailey", "style": "analytical, skeptical, provides counterpoints", "role": "Co-Host"},
    "host_c": {"name": "Casey", "style": "expert, technical, provides depth", "role": "Expert"},
    "host_d": {"name": "Drew", "style": "devil's advocate, explores edge cases", "role": "Guest"}
}

def determine_speaker_count(word_count: int) -> int:
    """Determine number of speakers based on content length."""
    if word_count < 1000:
        return 2
    elif word_count < 3000:
        return 3
    else:
        return 4

def chunk_text(text: str, max_chars: int = 12000) -> list[str]:
    """Splits text into chunks."""
    chunks = []
    current_chunk = []
    current_length = 0
    
    paragraphs = text.split("\n\n")
    
    for para in paragraphs:
        if current_length + len(para) > max_chars:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_length = len(para)
        else:
            current_chunk.append(para)
            current_length += len(para)
    
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
        
    return chunks

def generate_dialogue_segment(
    chunk_text: str, 
    chunk_index: int, 
    total_chunks: int, 
    personas: list[dict],
    target_words: int,
    llm_config: dict
) -> list[dict]:
    """Generates a dialogue segment for a specific chunk of text."""
    
    is_first = (chunk_index == 0)
    is_last = (chunk_index == total_chunks - 1)
    
    context_instruction = ""
    # Distribute words evenly across chunks
    segment_target = target_words // total_chunks if total_chunks > 0 else target_words

    if is_first and is_last:
        context_instruction = "This is the ONLY segment. Include a brief intro and a sign-off."
        segment_target = target_words
    elif is_first:
        context_instruction = "This is the FIRST segment of a multi-part series. Start with a brief intro, but DO NOT sign off. End with a transition to the next topic."
    elif is_last:
        context_instruction = "This is the FINAL segment. Start directly (no intro), wrap up the discussion, and give a sign-off."
    else:
        context_instruction = "This is a MIDDLE segment. Start directly (no intro) and end with a transition. DO NOT sign off."

    # Prompt construction
    prompt = f"""
    You are an expert podcast script writer. Create a natural, conversational dialogue based on the provided text chunk.
    
    **The Team:**
    {json.dumps(personas, indent=2)}
    
    **Context & Instructions:**
    - {context_instruction}
    - Target approximately {segment_target} words of dialogue for this segment.
    - Maintain reliable information from the text.
    - Use natural interruptions and reactions.
    - STRICTLY output valid JSON array of objects.
    
    **Source Text:**
    {chunk_text[:15000]}
    
    **Output Format (JSON):**
    [
        {{"speaker": "Alex", "text": "..."}},
        {{"speaker": "Bailey", "text": "..."}}
    ]
    """
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON array of objects."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        response_text = query_llm(
            messages=messages,
            provider=llm_config["provider"],
            model_name=llm_config["model_name"],
            api_key=llm_config.get("api_key"),
            local_pipeline=llm_config.get("local_pipeline")
        )
        
        # Clean up response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
             response_text = response_text.split("```")[1].strip()

        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        else:
             print(f"JSON parsing failed for chunk {chunk_index}. Raw: {response_text[:100]}...")
             return []
        
    except Exception as e:
        print(f"Error generating segment {chunk_index}: {e}")
        return []

def generate_script(content: dict, duration_minutes: int, llm_config: dict) -> dict:
    """Generates a full podcast script by chunking content and aggregating dialogues."""

    full_text = content.get("combined_content", "")
    
    # Target words calculation based on user request: 300 words/2 min => 150 wpm
    wpm = 150
    total_target_words = duration_minutes * wpm

    # Chunking
    chunk_size = 6000 if llm_config["provider"] == PROVIDER_LOCAL else 12000
    chunks = chunk_text(full_text, max_chars=chunk_size)
    
    print(f"Processing {len(chunks)} chunks... Target total words: {total_target_words}")
    
    num_speakers = determine_speaker_count(content.get("total_word_count", 0))
    active_personas = [PERSONAS["host_a"], PERSONAS["host_b"]]
    if num_speakers >= 3:
        active_personas.append(PERSONAS["host_c"])
    if num_speakers >= 4:
        active_personas.append(PERSONAS["host_d"])
    
    all_dialogue = []
    
    # Check if streamlit is active (for progress bar)
    is_streamlit = False
    try:
        import streamlit as st
        # Simple check if we are in a streamlit thread
        if st.runtime.exists():
            is_streamlit = True
    except:
        pass

    my_bar = None
    if is_streamlit:
        my_bar = st.progress(0, text="Generating script segments...")

    for i, chunk in enumerate(chunks):
        if my_bar:
            progress = (i / len(chunks))
            my_bar.progress(progress, text=f"Generating segment {i+1}/{len(chunks)}")
        
        segment_dialogue = generate_dialogue_segment(
            chunk_text=chunk,
            chunk_index=i,
            total_chunks=len(chunks),
            personas=active_personas,
            target_words=total_target_words, 
            llm_config=llm_config
        )
        
        if segment_dialogue:
             all_dialogue.extend(segment_dialogue)
    
    if my_bar:
        my_bar.empty()
    
    return {
        "title": content.get("title", "Podcast Episode"),
        "speakers": [p["name"] for p in active_personas],
        "duration_target": duration_minutes,
        "dialogue": all_dialogue
    }
