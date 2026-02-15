# 🎙️ Synth-FM: AI-Powered Podcast Generator

Synth-FM transforms web articles and documents into engaging, multi-speaker podcasts using AI.

## Features
- **Multi-Source Input**: URLs, PDFs, DOCX, Text files.
- **AI Personas**: 2-4 distinct speakers.
- **LLM**: Google Gemini 1.5 Flash (Fast & Efficient).
- **TTS**: Edge TTS (High-quality Neural Voices).
- **Post-Processing**: Seamless transitions with crossfades.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd synth-fm
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (Required for audio processing):
   - **Linux**: `sudo apt install ffmpeg`
   - **Mac**: `brew install ffmpeg`
   - **Windows**: Download and add to PATH.

4. **Set up API Key**:
   - Copy `.env.template` to `.env`:
     ```bash
     cp .env.template .env
     ```
   - Add your `GEMINI_API_KEY` in `.env` (Get from Google AI Studio).

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

1. **Add Content**: Paste URLs or upload files.
2. **Process**: Extract text.
3. **Generate Script**: Create dialogue with Gemini.
4. **Synthesize**: Generate audio with Edge TTS.
5. **Assemble**: Download final podcast.

## License
MIT
