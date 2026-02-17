# 🎙️ Synth-FM: AI-Powered Podcast Generator

> **Turn your reading list into an engaging, multi-speaker podcast.**

![Synth-FM Banner](https://placeholder.com/banner.png) *(Replace with actual banner/screenshot)*

**Synth-FM** is an advanced AI audio synthesis platform that transforms written content—articles, research papers, documentation, and blog posts—into professional-quality podcasts. It leverages state-of-the-art LLMs (OpenAI, Gemini, Local Llama) to generate natural, conversational scripts and high-fidelity TTS (Kokoro) to bring them to life with multiple distinct speakers.

## ✨ Key Features

-   **🗣️ Natural Multi-Speaker Conversations**: Automatically generates dynamic dialogue between 2-4 hosts (e.g., The Enthusiast, The Skeptic, The Expert).
-   **📚 Multi-Source Ingestion**:
    -   **URLs**: Paste links from Medium, Substack, News sites, etc.
    -   **Documents**: Upload PDF, DOCX, TXT, or MD files.
-   **🧠 Intelligent Script Generation**: Uses advanced prompt engineering to create engaging scripts with humor, debate, and insight.
-   **🎧 High-Fidelity Audio**: Powered by **Kokoro TTS** for realistic voice synthesis that rivals human speech.
-   **⚡ Modern Architecture**: Built with a robust **FastAPI** backend and a reactive **React + Vite** frontend.
-   **🤖 flexible AI Models**:
    -   **Cloud**: OpenAI (GPT-4o), Google Gemini 1.5.
    -   **Local**: Run completely offline with Llama 3.2 and local TTS (requires GPU).

## 🛠️ Tech Stack

### Frontend
-   **Framework**: [React](https://react.dev/) + [Vite](https://vitejs.dev/)
-   **Styling**: [Tailwind CSS](https://tailwindcss.com/) + [Lucide React](https://lucide.dev/) (Icons)
-   **State Management**: React Hooks
-   **HTTP Client**: Axios

### Backend
-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
-   **Server**: Uvicorn
-   **AI Orchestration**: LangChain (implied/custom logic)
-   **TTS**: Kokoro (Onnx/PyTorch)
-   **Data Processing**: Trafilatura (Scraping), PyPDF2, python-docx

## 🚀 Installation & Setup

Follow these steps to get Synth-FM running locally.

### Prerequisites
-   **Python 3.10+** (Conda recommended)
-   **Node.js v18+** & `npm`
-   **Git**
-   *(Optional)* **NVIDIA GPU** for local model inference.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/synth-fm.git
cd synth-fm
```

### 2️⃣ Backend Setup

We recommend using Conda to manage dependencies, especially for GPU support.

```bash
# Create and activate the environment
conda env create -f backend/environment.yml
conda activate synth-fm-gpu

# Alternatively, using pip:
# pip install -r backend/requirements.txt
```

**Set up Environment Variables:**

Create a `.env` file in the root directory (copy from `.env.template` if available):

```bash
cp .env.template .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
HF_TOKEN=... (Optional, for gated models)
```

**Start the Backend Server:**

```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`. Documentation at `http://localhost:8000/docs`.

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

## 📖 Usage Guide

1.  **Open the App**: Navigate to `http://localhost:5173`.
2.  **Configure Podcast**:
    -   **Duration**: Select 2, 5, or 10 minutes.
    -   **Model**: Choose between OpenAI, Gemini, or Local.
    -   **Speakers**: Select your host personalities.
3.  **Add Content**:
    -   Paste URLs into the input field.
    -   Or drag & drop PDF/DOCX files.
4.  **Generate**: Click **"Generate Podcast"**.
    -   *Step 1*: Content is extracted and cleaned.
    -   *Step 2*: LLM generates a script.
    -   *Step 3*: TTS synthesizes audio.
5.  **Listen & Download**: Play the podcast in the built-in player or download the `.wav`/`.mp3` file.

## 📂 Project Structure

```
synth-fm/
├── backend/                # FastAPI Application
│   ├── api/                # API Routes (Endpoints)
│   ├── utils/              # Core Logic (LLM, TTS, Extraction)
│   ├── main.py             # App Entry Point
│   └── environment.yml     # Conda Environment
├── frontend/               # React Application
│   ├── src/
│   │   ├── components/     # Reusable UI Components
│   │   ├── pages/          # Page Views
│   │   └── App.jsx         # Main Component
│   ├── package.json        # Frontend Dependencies
│   └── vite.config.js      # Vite Configuration
├── data/                   # Data Storage (Temp)
│   ├── temp/               # Temporary Audio Segments
│   └── output/             # Final Podcasts
├── README.md               # Project Documentation
└── LICENSE                 # MIT License
```

## 🗺️ Roadmap

- [ ] **Mobile App**: React Native version for on-the-go listening.
- [ ] **RSS Feeds**: Personal podcast feeds for generated content.
- [ ] **Voice Cloning**: Upload your own voice sample for a host.
- [ ] **User Accounts**: Save history and preferences.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Built with ❤️ by Akshay SG.**
