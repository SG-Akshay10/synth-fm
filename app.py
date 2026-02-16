import streamlit as st
import os
import nest_asyncio
from utils.llm import (
    get_local_model_pipeline, 
    PROVIDER_OPENAI, 
    PROVIDER_GEMINI, 
    PROVIDER_LOCAL,
    MODEL_GEMINI_FLASH,
    MODEL_GEMINI_PRO,
    MODEL_LOCAL_3B,
    MODEL_LOCAL_1B,
    unload_local_model
)

# Apply nest_asyncio to allow async loop in Streamlit
nest_asyncio.apply()

st.set_page_config(page_title="Synth-FM", page_icon="🎙️", layout="wide")

st.title("🎙️ Synth-FM: AI Podcast Generator")
st.markdown("Turn your reading list into an engaging podcast.")

# Session state initialization
if "url_inputs" not in st.session_state:
    st.session_state.url_inputs = [""]

if "extracted_content" not in st.session_state:
    st.session_state.extracted_content = None

if "generated_script" not in st.session_state:
    st.session_state.generated_script = None

if "audio_segments" not in st.session_state:
    st.session_state.audio_segments = []

if "final_audio_path" not in st.session_state:
    st.session_state.final_audio_path = None

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")
    
    # Model Selection
    st.subheader("🤖 Model Provider")
    provider = st.radio(
        "Select Provider",
        options=[PROVIDER_OPENAI, PROVIDER_GEMINI, PROVIDER_LOCAL],
        index=2 # Default to Local
    )
    
    llm_config = {"provider": provider}
    
    if provider == PROVIDER_OPENAI:
        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        model_name = st.selectbox("Model", ["gpt-4o", "gpt-3.5-turbo"])
        llm_config["api_key"] = api_key
        llm_config["model_name"] = model_name
        
    elif provider == PROVIDER_GEMINI:
        api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
        model_name = st.selectbox("Model", [MODEL_GEMINI_FLASH, MODEL_GEMINI_PRO])
        llm_config["api_key"] = api_key
        llm_config["model_name"] = model_name
        
    elif provider == PROVIDER_LOCAL:
        model_name = st.selectbox("Local Model", [MODEL_LOCAL_3B,MODEL_LOCAL_1B])
        llm_config["model_name"] = model_name
        st.info("First run will download model weights.")
        
        # Load model immediately if local selected
        # Button to trigger model loading
        if "loaded_model_name" not in st.session_state:
            st.session_state.loaded_model_name = None
            
        if st.button("Load Model"):
            with st.spinner(f"Loading {model_name}..."):
                pipe = get_local_model_pipeline(model_name)
                if pipe:
                    st.session_state.local_pipeline = pipe
                    st.session_state.loaded_model_name = model_name
                else:
                    st.error("Failed to load model")

        # Persist pipeline if loaded and matches selected model
        if st.session_state.get("local_pipeline") and st.session_state.loaded_model_name == model_name:
            st.success(f"Model Loaded: {model_name}")
            llm_config["local_pipeline"] = st.session_state.local_pipeline
        elif st.session_state.get("local_pipeline"):
             st.warning(f"Loaded: {st.session_state.loaded_model_name}. Click 'Load Model' to switch to {model_name}.")

    st.divider()
    
    duration = st.select_slider(
        "Podcast Duration",
        options=[2, 3, 5],
        value=2,
        format_func=lambda x: f"{x} Minutes"
    )
    
    num_speakers = st.slider(
        "Number of Speakers",
        min_value=2,
        max_value=4,
        value=2,
        help="Select between 2 to 4 speakers for the podcast."
    )
    
    st.divider()
    st.subheader("📝 Podcast Details")
    podcast_name = st.text_input("Podcast Name", value="Synth-FM")
    
    st.caption("Speaker Names")
    speaker_names = []
    default_names = ["Alex", "Bailey", "Casey", "Devin"]
    for i in range(num_speakers):
        name = st.text_input(f"Speaker {i+1}", value=default_names[i], key=f"speaker_name_{i}")
        speaker_names.append(name)
    

    st.divider()
    st.markdown("### 🛠️ Instructions")
    st.markdown("""
    1. **Add Content**: URLs or Documents
    2. **Process**: Extract text
    3. **Script**: Generate dialogue
    4. **Audio**: Synthesize voices
    5. **Download**: Get your MP3
    """)


# Input Section
st.header("1. Add Content")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔗 URLs")
    
    # Dynamic URL inputs
    for i, url in enumerate(st.session_state.url_inputs):
        st.session_state.url_inputs[i] = st.text_input(
            f"URL {i+1}", 
            value=url,
            key=f"url_{i}",
            placeholder="https://example.com/article"
        )
    
    # Add/Remove URL buttons
    b_col1, b_col2 = st.columns([1, 1])
    with b_col1:
        if st.button("➕ Add URL"):
            st.session_state.url_inputs.append("")
            st.rerun()
    with b_col2:
        if len(st.session_state.url_inputs) > 1:
            if st.button("➖ Remove URL"):
                st.session_state.url_inputs.pop()
                st.rerun()

with col2:
    st.subheader("📄 Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, TXT, or MD files",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True
    )

# Process Button
st.divider()
urls_provided = any(u.strip() for u in st.session_state.url_inputs)
files_provided = bool(uploaded_files)

process_disabled = not (urls_provided or files_provided)

from utils import (
    extract_from_url,
    extract_from_pdf,
    extract_from_docx,
    extract_from_text,
    aggregate_content
)

if st.button("🚀 Process Content", disabled=process_disabled, type="primary"):
    with st.spinner("Extracting content..."):
        aggregated_sources = []
        
        # Process URLs
        for url in st.session_state.url_inputs:
            if url.strip():
                result = extract_from_url(url)
                aggregated_sources.append(result)
        
        # Process Files
        if uploaded_files:
            for file in uploaded_files:
                ext = file.name.split(".")[-1].lower()
                if ext == "pdf":
                    result = extract_from_pdf(file)
                elif ext == "docx":
                    result = extract_from_docx(file)
                elif ext in ["txt", "md"]:
                    result = extract_from_text(file)
                else:
                    continue 
                aggregated_sources.append(result)
        
        # Aggregate Results
        final_content = aggregate_content(aggregated_sources)
        st.session_state.extracted_content = final_content

# Display Content if available
if st.session_state.extracted_content:
    final_content = st.session_state.extracted_content
    st.divider()
    st.header("2. Extracted Content")
    
    if final_content.get("valid"):
        st.success(f"✅ Ready for script generation! ({final_content['total_word_count']} words)")
        with st.expander("View Source Content"):
            st.text_area("Content Preview", final_content["combined_content"], height=300)
    else:
        st.error(f"⚠️ {final_content.get('error')}")
        st.write("Sources Summary:")
        for summary in final_content.get("sources_summary", []):
            st.write(summary)
    
    if final_content.get("valid"):
        from utils import generate_script
        
        st.divider()
        st.header("3. Generate Script")
        
        if st.button("📝 Generate Podcast Script", type="primary"):
            # Validation for keys
            if provider == PROVIDER_OPENAI and not api_key:
                st.error("Please enter an OpenAI API Key.")
            elif provider == PROVIDER_GEMINI and not api_key:
                st.error("Please enter a Gemini API Key.")
            elif provider == PROVIDER_LOCAL and "local_pipeline" not in llm_config:
                 st.error("Please load the local model first.")
            else:
                if final_content['total_word_count'] > 1500: # Approx 8000 chars
                    st.info("ℹ️ Large content detected. Automatic summarization enabled (this may take a moment).")
                    
                with st.spinner(f"Generating script using {provider}..."):
                    script = generate_script(final_content, duration, llm_config, num_speakers, podcast_name, speaker_names)
                    st.session_state.generated_script = script
        
        # Display Script
        if st.session_state.generated_script:
            script = st.session_state.generated_script
            
            if "error" in script:
                st.error(script["error"])
            else:
                st.success(f"✅ Script Generated: {script.get('title', 'Podcast')}")
                
                with st.expander("View Script", expanded=True):
                    # Create a tuple of unique speakers from the dialogue
                    unique_speakers = []
                    for turn in script.get("dialogue", []):
                        s = turn.get("speaker")
                        if s and s not in unique_speakers:
                            unique_speakers.append(s)
                    speaker_names_tuple = tuple(unique_speakers)
                    
                    for turn in script.get("dialogue", []):
                        speaker = turn.get("speaker") or "Unknown"
                        text = turn.get("text", "")
                        
                        # Map speaker to color based on index
                        try:
                            idx = speaker_names_tuple.index(speaker)
                            colors = ["blue", "green", "orange", "red"]
                            color = colors[idx % len(colors)]
                        except ValueError:
                            color = "gray"
                            
                        st.markdown(f"**:{color}[{speaker}]:** {text}")

            from utils import batch_synthesize_audio
            
            st.divider()
            st.header("4. Generate Audio")
            
            if st.button("🗣️ Synthesize Audio", type="primary"):
                # Unload local model if provider is local to free up memory for TTS
                if provider == PROVIDER_LOCAL:
                    smi_output = unload_local_model()
                    if smi_output:
                        with st.expander("📊 NVIDIA GPU Status (After Unload)", expanded=False):
                            st.code(smi_output)
                    
                with st.spinner("Synthesizing audio segments using Kokoro..."):
                    audio_paths = batch_synthesize_audio(script,unique_speakers)
                    st.session_state.audio_segments = audio_paths
            
            if st.session_state.audio_segments:
                st.success(f"✅ Generated {len(st.session_state.audio_segments)} audio segments!")
                st.info("Validation complete. Ready for final assembly.")
                
                from utils import create_podcast
                
                st.divider()
                st.header("5. Final Assembly")
                
                if st.button("💿 Create Final Podcast", type="primary"):
                    with st.spinner("Stitching and normalizing audio..."):
                        final_path = create_podcast(st.session_state.audio_segments)
                        st.session_state.final_audio_path = final_path
                        
                if st.session_state.final_audio_path:
                    st.success("✅ Podcast Ready!")
                    st.audio(st.session_state.final_audio_path)
                    
                    with open(st.session_state.final_audio_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Podcast (WAV)",
                            data=f,
                            file_name="synth_fm_podcast.wav",
                            mime="audio/wav"
                        )