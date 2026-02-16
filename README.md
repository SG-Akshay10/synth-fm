# Synth-FM: AI Podcast Generator

Turn your reading list into an engaging podcast using local or cloud LLMs and high-quality TTS.

## 🚀 New Architecture

This project has been migrated to a modern web stack:
- **Backend**: FastAPI (Python) for AI/ML operations.
- **Frontend**: React + Vite + Tailwind CSS for a responsive UI.
- **AI Models**: Support for Local LLMs (Llama 3.2), OpenAI, and Gemini.

## 🛠️ Setup Instructions

### Prerequisites
- Conda (Miniconda or Anaconda)
- Node.js (v18+)

### 1. Backend Setup

```bash
# Create and activate the conda environment
conda env create -f backend/environment.yml
conda activate synth-fm-gpu

# Start the Backend Server
uvicorn backend.main:app --reload
```
The backend API will run at `http://localhost:8000`.

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the Development Server
npm run dev
```
The frontend UI will run at `http://localhost:5173`.

## 📝 Usage

1.  **Select Provider**: Choose between Local LLM, OpenAI, or Gemini.
2.  **Configuration**: Set API keys (if needed) and customize podcast duration/speakers.
3.  **Add Content**: Paste URLs or upload documents (PDF, DOCX, TXT).
4.  **Process**: Click "Process Content" to extract text.
5.  **Generate Script**: Create a dialogue script from the content.
6.  **Synthesize**: Generate audio using Kokoro TTS (high quality).
7.  **Listen**: Play the final podcast directly in the browser or download the WAV file.

## 📁 Project Structure

- `backend/`: FastAPI application code.
    - `api/endpoints/`: API route handlers.
    - `utils/`: Core logic for extraction, LLM, and TTS.
- `frontend/`: React application code.
    - `src/`: Components and logic.

## ⚠️ Notes
- The "Local" provider requires a GPU with sufficient VRAM (approx 4GB-8GB depending on model).
- First run with Local LLM or Kokoro TTS will download model weights.
