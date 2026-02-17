
# 🎙️ Synth-FM: AI-Powered Podcast Generator

> **Turn your reading list into an engaging, multi-speaker podcast.**

![Likely Banner Placeholder](https://placehold.co/1200x400/1e1e1e/FFF?text=Synth-FM+Architecture&font=roboto)

**Synth-FM** is an advanced AI audio synthesis platform that transforms written content—articles, research papers, documentation, and blog posts—into professional-quality podcasts. It orchestrates a pipeline of state-of-the-art technologies:
*   **LLMs** (OpenAI, Gemini, Groq, Local Llama) script the conversation.
*   **Kokoro TTS** (High-Fidelity) synthesizes realistic voices.
*   **FastAPI & React** provide a seamless, modern user experience.

---

## ✨ Key Features

-   **🗣️ Natural Multi-Speaker Conversations**: Automatically generates dynamic dialogue between hosts (e.g., *The Enthusiast*, *The Skeptic*, *The Expert*) with distinct personalities.
-   **📚 Multi-Source Ingestion**:
    -   **URLs**: Paste links from Medium, Substack, News sites, etc.
    -   **Documents**: Upload PDF, DOCX, TXT, or MD files.
-   **🤖 Flexible AI Models**:
    -   **Cloud**: OpenAI (GPT-4o), Google Gemini 1.5 Flash/Pro, Groq (Llama 3 8b).
    -   **Local**: Run completely offline with **Llama 3.2 (1B/3B)** and **Qwen 2.5** (requires GPU).
-   **🎧 High-Fidelity Audio**: Powered by **Kokoro TTS** (via Onnx/PyTorch) for realistic voice synthesis that rivals human speech.
-   **⚡ Modern Architecture**: Built with a robust **FastAPI** backend and a reactive **React + Vite** frontend.
-   **🧠 Memory Management**: Smart VRAM management to load/unload local LLM models dynamically during generation.

---

## 🏗️ System Architecture

The following diagram illustrates the data flow from user input to the final podcast audio file.

```mermaid
graph TD
    User[User] -->|Uploads File/URL| Frontend[React Frontend]
    Frontend -->|POST /api/content/*| Backend[FastAPI Backend]
    
    subgraph "Backend Processing"
        Backend -->|Extract Text| Extractor[Content Extractor]
        Extractor -->|Raw Text| LLM_Service[LLM Service]
        
        subgraph "AI Script Generation"
            LLM_Service -->|Prompt| OpenAI[OpenAI GPT-4]
            LLM_Service -->|Prompt| Gemini[Google Gemini]
            LLM_Service -->|Prompt| Local[Local LLM (Llama/Qwen)]
            Local -.->|Load/Unload| VRAM[GPU VRAM]
        end
        
        LLM_Service -->|Generated Script JSON| Backend
        Backend -->|Script Segments| TNT[TTS Controller]
        
        subgraph "Audio Synthesis"
            TNT -->|Text| Kokoro[Kokoro TTS Model]
            Kokoro -->|Waveform| AudioUtil[Audio Processor]
            AudioUtil -->|Stitch Segments| FinalAudio[Final Podcast .wav]
        end
    end
    
    Backend -->|Audio File URL| Frontend
    Frontend -->|Play/Download| User
```

---

## 🛠️ Tech Stack

### Frontend
-   **Framework**: [React](https://react.dev/) + [Vite](https://vitejs.dev/)
-   **Styling**: [Tailwind CSS](https://tailwindcss.com/) + [Lucide React](https://lucide.dev/) (Icons)
-   **State Management**: React Hooks
-   **HTTP Client**: Axios

### Backend
-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
-   **Server**: Uvicorn
-   **AI Orchestration**: Custom Python Modules (`utils/llm.py`)
-   **TTS**: **Kokoro** (High-quality offline TTS)
-   **Data Processing**: `Trafilatura` (Web Scraping), `PyPDF2`, `python-docx`

---

## 🔌 Backend API Documentation

The backend exposes several key endpoints for the synthesis pipeline.

### 1. Content Extraction
**Endpoint**: `POST /api/content/extract-urls`
*   **Description**: Scrapes text content from a list of URLs.
*   **Payload**: `{"urls": ["https://example.com/article"]}`
*   **Response**: `{"title": "...", "text": "...", "source": "url"}`

**Endpoint**: `POST /api/content/extract-files`
*   **Description**: Extracts text from uploaded files (PDF, DOCX, TXT).
*   **Payload**: `multipart/form-data` (file upload)

### 2. Script Generation
**Endpoint**: `POST /api/script/generate-script`
*   **Description**: Uses an LLM to turn the extracted content into a podcast script.
*   **Payload**:
    ```json
    {
        "content_data": "Extracted text...",
        "duration": "short", // or "medium", "long"
        "provider": "openai", // "gemini", "groq", "local"
        "model_name": "gpt-4o",
        "api_key": "sk-...",
        "num_speakers": 2,
        "tone": "humorous"
    }
    ```
*   **Response**: JSON object representing the dialogue script.

### 3. Audio Synthesis
**Endpoint**: `POST /api/audio/synthesize-audio`
*   **Description**: Generates audio segments for each line of dialogue using Kokoro TTS.
*   **Payload**: The script JSON generated in the previous step.
*   **Storage**: Saves temporary `.wav` files in `data/temp/`.

**Endpoint**: `POST /api/audio/create-podcast`
*   **Description**: Stitches all temporary audio segments into a single file.
*   **Response**: Path to the final `.wav` file.

### 4. Model Management (Local Only)
**Endpoint**: `POST /api/model/load`
*   **Description**: Loads a local LLM into VRAM.
*   **Payload**: `{"model_name": "local_3b"}`

**Endpoint**: `POST /api/model/unload`
*   **Description**: Unloads the local LLM to free up VRAM for TTS operations.

---

## 🚀 Installation & Setup

### Prerequisites
-   **Python 3.10+** (Conda recommended for GPU isolation)
-   **Node.js v18+** & `npm`
-   **Git**
-   *(Optional)* **NVIDIA GPU** (8GB+ VRAM recommended for local inference)
-   **FFmpeg** (Required for audio processing: `sudo apt install ffmpeg`)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/synth-fm.git
cd synth-fm
```

### 2️⃣ Backend Setup

We recommend using Conda to manage dependencies.

```bash
# Create and activate the environment
conda env create -f backend/environment.yml
conda activate synth-fm-gpu

# Navigate to root directory
# Create .env file
cp .env.template .env
```

**Configure `.env`:**
Edit `.env` and add your API keys. If using local models, `HF_TOKEN` is required for gated models like Llama 3.

```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
GROQ_API_KEY=gsk_...
HF_TOKEN=hf_... 
```

**Start the Backend:**

```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 3️⃣ Frontend Setup

Open a new terminal window.

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```
The UI will be running at `http://localhost:5173`.

---

## 📖 Usage Guide

1.  **Select Your Content**: Paste URLs or upload documents/PDFs on the landing page.
2.  **Configure Settings**:
    *   **LLM Provider**: Choose Cloud (OpenAI/Gemini/Groq) for speed, or Local for privacy.
    *   **Podcast Style**: set the tone (Funny, Serious, Debate).
    *   **Duration**: Choose how long you want the episode to be.
3.  **Generate Script**: Click "Generate". The AI will draft a conversation. *You can review the script before synthesis.*
4.  **Synthesize Audio**: The system will use Kokoro TTS to voice the script.
    *   *Note: If using local models, the LLM will unload first to free VRAM for TTS.*
5.  **Listen & Share**: Play the final podcast in the built-in player or download it.

---

## 📂 Project Structure

```
synth-fm/
├── backend/                # FastAPI Application & Logic
│   ├── api/                # API Routers (endpoints)
│   ├── utils/              # Core Logic (LLM, TTS, Extraction)
│   ├── main.py             # Entry Point
│   └── environment.yml     # Dependencies
├── frontend/               # React Application
│   ├── src/
│   │   ├── components/     # UI Components
│   │   ├── pages/          # Screens
│   │   └── lib/            # Utilities
├── data/                   # Local Storage
│   ├── temp/               # Temporary Audio Segments
│   └── output/             # Final Podcasts
└── README.md               # You are here
```

---

## 🗺️ Roadmap

- [ ] **Mobile App**: React Native version.
- [ ] **RSS Feeds**: Personal podcast feeds.
- [ ] **Voice Cloning**: Fine-tune TTS with custom voice samples.
- [ ] **User Accounts**: History and preferences.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Built with ❤️ by Akshay SG.**
