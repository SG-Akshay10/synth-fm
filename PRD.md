**Product Requirements Document**

**Synth-FM: AI-Powered Audio Content Generation**

  ----------------- -----------------------------------------------------
  **Version**       1.0

  **Date**          February 15, 2026

  **Status**        Draft
  ----------------- -----------------------------------------------------

---

## Quick Start Guide

**For AI Agents/Developers:** 
1. Read Section 1-5 for context
2. **Start implementation at Section 9.4** (Step-by-Step Implementation)
3. Follow stages sequentially: 0 → 1 → 2 → 3 → 4 → 5
4. Do NOT skip validation steps

**MVP Goal:** Working local demo in 2-3 days
**Production Goal:** Free-tier hosted app in 1-2 weeks

---

1\. Executive Summary

Synth-FM is an AI-powered audio synthesis platform that transforms written content into engaging, conversational podcasts. Similar to Google's NotebookLM audio feature, this tool enables users to upload documents or paste URLs and receive a professionally produced podcast discussion featuring 2-4 AI personas engaging in natural conversation.

The platform addresses the growing demand for audio content consumption by automatically converting blog posts, documentation, articles, and uploaded documents into accessible, conversation-style podcasts that users can listen to on-the-go. Podcast duration is flexible (2-5 minutes), with current MVP targeting 2-3 minute outputs due to resource constraints.

2\. Problem Statement

2.1 Market Need

-   Content consumers increasingly prefer audio formats but most valuable online content exists only in written form

-   Reading long-form articles requires dedicated time and attention that many users cannot afford in their busy schedules

-   Standard text-to-speech solutions produce monotonous, single-voice output that lacks engagement

-   Creating professional podcasts manually requires significant time, expertise, and resources

2.2 User Pain Points

-   Users want to consume content during commutes, workouts, or other activities where reading is impractical

-   Educational and technical content often requires multiple readings to fully understand

-   Users struggle to stay engaged with dense written material but find conversations more accessible

3\. Product Vision & Goals

3.1 Vision Statement

To democratize audio content creation by enabling anyone to transform written material into engaging, professional-quality podcasts instantly, making knowledge more accessible and consumable for all learning styles.

3.2 Primary Goals

-   Generate natural, conversational podcast content from URLs and uploaded documents (PDF, DOCX, TXT, MD)

-   Produce 2-5 minute podcasts with 2-4 distinct, engaging AI personas in under 2 minutes (MVP targets 2-3 minutes)

-   Achieve 90%+ user satisfaction with audio quality and conversation naturalness

-   Support processing of multiple URLs and documents simultaneously in a single session

-   Dynamically determine optimal number of speakers (2-4) based on content complexity and topic

4\. Target Users

4.1 Primary Personas

**The Busy Professional**

-   Age: 28-45, works in tech/business/finance

-   Needs to stay current with industry news and trends but has limited reading time

-   Consumes content during commutes, workouts, or while doing chores

**The Continuous Learner**

-   Age: 22-35, student or early-career professional

-   Consumes technical documentation, tutorials, and educational content regularly

-   Prefers audio learning for better retention and multi-tasking

**The Content Creator**

-   Age: 25-40, blogger, educator, or marketing professional

-   Wants to repurpose written content into audio format for broader reach

-   Lacks resources or skills to produce professional podcasts manually

5\. Functional Requirements

5.1 Core Features

5.1.1 Content Input & Extraction

**URL Input:**
-   Accept multiple valid web URLs as input (batch processing)

-   Extract main article content, filtering out ads, navigation, and irrelevant elements

-   Support for major content platforms: Medium, Substack, WordPress, documentation sites, news outlets

-   Validate URL accessibility and content quality before processing

**Document Upload:**
-   Accept document uploads: PDF, DOCX, TXT, MD formats

-   Support multiple document uploads in a single session

-   Extract and parse text content from uploaded documents

-   Combine content from multiple sources intelligently

**Content Processing:**
-   Handle combined content ranging from 500 to 5,000 words total

-   Merge multiple sources into coherent narrative for script generation

-   Maintain attribution and context from different sources

5.1.2 AI Script Generation

-   Generate conversational script featuring 2-4 distinct personas (determined by content complexity)

-   **Base Personas (Always Present):**
    -   Host A: Enthusiastic, curious, asks clarifying questions
    -   Host B: Skeptical, analytical, provides counterpoints and deeper analysis

-   **Optional Additional Personas (Based on Content):**
    -   Host C: Subject matter expert, provides technical depth
    -   Host D: Devil's advocate, challenges assumptions and explores edge cases

-   Dynamic speaker allocation based on:
    -   Content complexity (technical vs. general)
    -   Topic diversity (multiple perspectives needed)
    -   Word count (longer content may benefit from more voices)

-   Script structure includes: introduction, key points discussion, implications/analysis, and conclusion

-   Natural conversation flow with interruptions, agreements, and transitions

-   **Flexible duration:** 2-5 minutes based on content length
    -   2 minutes: ~300-400 words of dialogue (MVP default)
    -   3 minutes: ~450-550 words of dialogue
    -   5 minutes: ~750-850 words of dialogue (resource-intensive)

5.1.3 Text-to-Speech Synthesis

-   Convert script to high-quality audio using TTS API (OpenAI TTS or ElevenLabs)

-   Support 2-4 distinct voice profiles based on number of personas:
    -   Voice variety: different gender, accent, tone, and speaking style
    -   Voice consistency: same persona always uses same voice

-   Process dialogue lines in parallel to minimize generation time

-   Support for multiple audio output formats (MP3, WAV)

-   Audio quality: minimum 128 kbps, preferably 192 kbps

5.1.4 Audio Post-Processing

-   Seamlessly stitch individual audio segments using ffmpeg

-   Add subtle crossfades between speaker transitions (50-100ms)

-   Normalize audio levels across all segments

-   Optional: Add intro/outro music (5-10 seconds each)

-   Final file size optimization without quality loss

5.1.5 User Interface

-   **Framework:** Streamlit-based web interface (Python)

-   **Input Section:**
    -   Multiple URL input fields (add/remove dynamically)
    -   Document upload widget supporting multiple files (PDF, DOCX, TXT, MD)
    -   Clear visual feedback for each uploaded source
    -   Validation indicators for each input

-   **Configuration Options:**
    -   Podcast duration selector (2, 3, or 5 minutes)
    -   Optional: Number of speakers override (2-4)

-   Real-time progress indicator showing: content extraction, script generation, audio synthesis, post-processing

-   Audio player with play/pause, seek, and volume controls

-   Download button for final podcast file

-   Optional: Display generated script alongside audio player

-   Session state management to preserve inputs during processing

5.2 Optional Features (Post-MVP)

-   Custom persona selection (professional, casual, educational styles)

-   Adjustable podcast length (3, 5, 10, or 15 minutes)

-   Multi-article input for series generation

-   User accounts with podcast library and history

-   RSS feed generation for podcast subscriptions

-   Social sharing capabilities

-   Browser extension for one-click conversion

6\. Technical Architecture

6.1 System Components

6.1.1 Frontend

**MVP (Demo - Streamlit):**
-   **Framework:** Streamlit (Python-based)
    -   Rapid prototyping and development
    -   Built-in state management
    -   Native support for file uploads and progress bars
    -   Easy integration with Python backend
    -   **Purpose:** Quick demo and proof of concept

-   **UI Components:** Streamlit native components
    -   st.file_uploader for document uploads
    -   st.text_input for URLs
    -   st.progress for real-time updates
    -   st.audio for playback

-   **State Management:** Streamlit session state

-   **Audio Player:** Streamlit audio component with download capability

**Post-MVP (Production - Modern Web Stack):**
-   **Framework:** Next.js 14+ or Vite + React
-   **Styling:** Tailwind CSS
-   **UI Components:** shadcn/ui or Headless UI
-   **State Management:** Zustand or React Context
-   **Audio Player:** Howler.js or react-audio-player
-   **Backend Communication:** REST API or tRPC
-   **Why replace Streamlit:** 
    -   Better performance and user experience
    -   Custom branding and design
    -   Mobile-responsive design
    -   SEO optimization
    -   Production-ready scalability

**Migration Strategy:**
1. Keep backend logic in Python
2. Expose backend as FastAPI REST API
3. Build new frontend that calls the API
4. Both can run simultaneously during transition

6.1.2 Backend

**MVP (Simple & Local):**
-   **Framework:** Python with FastAPI (lightweight) or Flask
-   **No separate API server needed** - Streamlit handles UI and calls backend functions directly
-   **Task Queue:** None for MVP (synchronous processing is acceptable for demo)
-   **Web Scraping:** Trafilatura (simple, effective)
-   **Document Parsing:** 
    -   PyPDF2 for PDF
    -   python-docx for DOCX
    -   Direct file read for TXT/MD
-   **LLM Integration:** OpenAI API (GPT-4o-mini for cost efficiency)
-   **TTS Integration:** OpenAI TTS API (simple, good quality)
-   **Audio Processing:** pydub (Python-based, simple) with FFmpeg backend

**Post-MVP (Production):**
-   Add proper API with FastAPI
-   Add task queue (Celery + Redis) for async processing
-   Add caching layer
-   Optimize API calls and costs

6.1.3 Storage & Caching

**MVP (Local & Simple):**
-   **File Storage:** Local filesystem
    -   `data/temp/` - Temporary audio segments
    -   `data/output/` - Final podcast files
    -   Auto-cleanup after 24 hours
-   **No caching layer needed** for MVP
-   **No database needed** for MVP (stateless demo)

**Post-MVP (Production):**
-   File Storage: Free cloud options
    -   Cloudflare R2 (10GB free)
    -   Backblaze B2 (10GB free)
    -   Supabase Storage (1GB free)
-   Cache Layer: Redis (Upstash free tier)
-   Database: PostgreSQL (Supabase free tier or Railway)

6.1.4 Infrastructure

**MVP (Local Development):**
-   Hosting: Local machine (localhost)
-   No containerization needed initially
-   Simple Python virtual environment
-   Local file storage in project directory
-   Basic console logging (Python logging module)

**Post-MVP (Production):**
-   Hosting Options (Free Tier):
    -   **Backend/Models:** Hugging Face Spaces (free GPU), Google Colab (limited), or Railway (free tier)
    -   **Frontend:** Vercel, Netlify, or GitHub Pages (static)
    -   **API:** Render (free tier with sleep), Railway, or Fly.io (free tier)
-   Container: Docker (optional, for deployment only)
-   Storage: Local filesystem (MVP) → Cloud storage (post-MVP)
-   Logging: Python logging to file (MVP) → Cloud logging (post-MVP)

6.2 Processing Pipeline

**Stage 1: Content Input & Extraction**

1.  User submits URLs and/or uploads documents via Streamlit interface

2.  Backend validates:
    -   URL format and accessibility
    -   Document file types and sizes
    -   Total content volume

3.  **For URLs:**
    -   Web scraper fetches page content
    -   Content extractor parses main article text, removing boilerplate

4.  **For Documents:**
    -   PDF parser extracts text content
    -   DOCX parser reads document structure
    -   TXT/MD files read directly

5.  Content aggregation:
    -   Combine multiple sources intelligently
    -   Remove duplicates and redundancy
    -   Word count validation (500-5,000 words total)

**Stage 2: Script Generation**

6.  Content sent to LLM with prompt engineering for podcast script

7.  LLM generates structured dialogue with speaker labels

8.  Script parser validates format and extracts speaker turns

9.  Script stored temporarily for processing

**Stage 3: Audio Synthesis**

10. Script divided into individual speaker segments

11. Parallel TTS API calls for each segment (with rate limiting)

12. Audio files downloaded and temporarily stored

13. Quality validation of generated audio files

**Stage 4: Audio Post-Processing**

14. FFmpeg concatenates audio segments in sequence

15. Apply crossfades between segments

16. Normalize audio levels

17. Add intro/outro music if configured

18. Export final MP3 file

**Stage 5: Delivery**

19. Final podcast file uploaded to storage

20. Frontend notified of completion via WebSocket

21. User presented with audio player and download option

22. Temporary files cleaned up after delivery

7\. Technical Challenges & Solutions

7.1 Latency Management

**Challenge:** Generating 5 minutes of high-quality audio can take 60-120 seconds, risking UI freezes and poor user experience.

**Solutions:**

-   Implement asynchronous task queue (Celery + Redis) to handle processing in background

-   Use WebSocket or Server-Sent Events for real-time progress updates

-   Parallelize TTS API calls for different segments (respecting rate limits)

-   Implement connection pooling and keep-alive for API requests

-   Show estimated completion time based on content length

-   Provide intermediate playback of completed segments while processing continues

7.2 Audio Quality & Synchronization

**Challenge:** Ensuring seamless transitions between different audio segments and maintaining consistent quality.

**Solutions:**

-   Use FFmpeg filter complex for smooth crossfades (afade filter)

-   Apply audio normalization using loudnorm filter

-   Validate sample rate consistency (44.1kHz or 48kHz) across all segments

-   Add silence padding (200-300ms) between segments for natural conversation rhythm

-   Test with various TTS providers to identify best quality-to-speed ratio

7.3 Script Generation Quality

**Challenge:** Creating natural, engaging dialogue that accurately represents source content while maintaining distinct personas.

**Solutions:**

-   Develop comprehensive prompt engineering with clear persona definitions

-   Include examples of ideal conversations in system prompt (few-shot learning)

-   Implement JSON-structured output for reliable parsing

-   Add validation layer to ensure balanced speaking time between hosts

-   Use GPT-4 or similar high-capability model for better conversational flow

-   Implement fallback generation if initial script quality is poor

7.4 Content Extraction Reliability

**Challenge:** Accurately extracting main content from diverse website structures and formats.

**Solutions:**

-   Use specialized content extraction libraries (Trafilatura, Newspaper3k)

-   Implement multiple extraction strategies with fallbacks

-   Add content quality validation (minimum word count, paragraph structure)

-   Handle paywalls and authentication gracefully with clear error messages

-   Support direct text paste as alternative to URL input

7.5 API Rate Limiting & Costs

**Challenge:** Managing API costs and rate limits for LLM and TTS services.

**Solutions:**

-   Implement request batching and intelligent retries with exponential backoff

-   Cache generated scripts and audio for identical URLs (with TTL)

-   Set usage quotas per user/IP to prevent abuse

-   Monitor API usage and implement alerts for unusual patterns

-   Optimize script length to balance quality and TTS costs

8\. Non-Functional Requirements

8.1 Performance

-   **Total processing time by duration:**
    -   2-minute podcast: Under 60 seconds
    -   3-minute podcast: Under 90 seconds
    -   5-minute podcast: Under 120 seconds

-   Content extraction (URL + documents): Under 5 seconds per source

-   Script generation: 15-30 seconds

-   TTS synthesis (parallelized): 
    -   2 minutes: 25-40 seconds
    -   5 minutes: 45-75 seconds

-   Audio post-processing: 5-10 seconds

-   Streamlit app load: Under 2 seconds

-   Progress updates: Real-time with \<500ms latency

8.2 Reliability

-   System uptime: 99% availability

-   Successful completion rate: 95% for valid URLs

-   Graceful degradation on API failures with retry mechanisms

-   Automatic cleanup of failed jobs and orphaned files

-   Error logging and monitoring for all failures

8.3 Scalability

-   Support 100 concurrent users (MVP)

-   Horizontal scaling capability for backend workers

-   Queue system can handle 1000+ queued jobs

-   Storage system supports auto-scaling based on usage

8.4 Security

-   Input validation and sanitization for all URLs

-   HTTPS enforcement for all connections

-   API key encryption and secure storage

-   Rate limiting to prevent abuse and DDoS attacks

-   Content Security Policy (CSP) headers

-   Regular security audits and dependency updates

8.5 Usability

-   Mobile-responsive design supporting phones and tablets

-   Accessibility compliance (WCAG 2.1 Level AA)

-   Clear error messages with suggested actions

-   Minimal learning curve - no tutorial required

-   Browser compatibility: Chrome, Firefox, Safari, Edge (latest 2 versions)

9\. Success Metrics

9.1 Technical Metrics

-   Average processing time: \<120 seconds

-   Success rate: \>95% for valid content URLs

-   System uptime: \>99%

-   API error rate: \<2%

-   Audio quality score: \>4.0/5.0 (user ratings)

9.2 User Engagement Metrics

-   Daily active users (DAU): Target 100 within first month

-   Podcast completion rate: \>75% of generated podcasts listened to end

-   Download rate: \>40% of completed podcasts downloaded

-   Return user rate: \>30% within 7 days

-   Average session duration: \>5 minutes

9.3 Quality Metrics

-   User satisfaction score: \>4.0/5.0

-   Net Promoter Score (NPS): \>40

-   Script quality rating: \>3.5/5.0 (human evaluation)

-   Audio naturalness rating: \>4.0/5.0

-   Content accuracy: \>90% (compared to source material)

---

## 9.4 Implementation Methodology

### Agentic AI Development Approach

This project will be implemented using an **agentic AI development methodology**, where an AI agent (LLM) takes autonomous steps to implement features incrementally based on clear, structured instructions. The AI agent should:

1. **Understand the full context** before starting any implementation
2. **Break down tasks** into atomic, testable steps
3. **Implement incrementally** with validation at each stage
4. **Self-correct** when errors occur
5. **Document decisions** and code as it progresses

### Step-by-Step Implementation Instructions

**⚠️ CRITICAL INSTRUCTION FOR AI AGENT:**

You MUST implement this project incrementally, stage by stage. DO NOT attempt to implement multiple stages simultaneously. Each stage must be fully functional and tested before proceeding to the next.

---

### **STAGE 0: Project Setup & Environment** (Complete FIRST)

**Objective:** Set up the development environment with all necessary dependencies.

**AI Agent Tasks:**
1. Create project directory structure:
   ```
   Synth-FM/
   ├── app.py              # Streamlit main application
   ├── requirements.txt    # Python dependencies
   ├── config.py          # Configuration and API keys
   ├── utils/
   │   ├── __init__.py
   │   ├── content_extractor.py
   │   ├── script_generator.py
   │   ├── audio_synthesizer.py
   │   └── audio_processor.py
   ├── data/
   │   ├── temp/          # Temporary file storage
   │   └── output/        # Final podcast outputs
   └── tests/
       └── test_stage1.py
   ```

2. Create `requirements.txt` with **minimal** dependencies:
   ```
   streamlit>=1.30.0
   requests>=2.31.0
   trafilatura>=1.6.0
   PyPDF2>=3.0.0
   python-docx>=1.1.0
   openai>=1.10.0
   pydub>=0.25.0
   python-dotenv>=1.0.0
   ```
   **Note:** No database, no Redis, no Celery for MVP - keep it simple!

3. Create `.env.template` for API keys:
   ```
   OPENAI_API_KEY=your_key_here
   ```

4. Initialize Git repository and create `.gitignore`

5. Test environment: Create minimal `app.py` with "Hello World" Streamlit app

**Validation Criteria:**
- [ ] All directories created
- [ ] Dependencies install without errors
- [ ] Streamlit app runs on `streamlit run app.py`
- [ ] Git repository initialized

**DO NOT PROCEED TO STAGE 1 UNTIL STAGE 0 IS VALIDATED.**

---

### **STAGE 1: Input Interface & Content Extraction** (Implement SECOND)

**Objective:** Create Streamlit UI that accepts multiple URLs and documents, then extracts and combines their content.

**AI Agent Tasks:**

**Part 1A: Build Streamlit Input Interface**
1. Create main `app.py` with:
   - Title and description
   - Session state initialization
   - Sidebar for configuration (podcast duration: 2/3/5 minutes)

2. Add URL input section:
   - Dynamic list of URL input fields
   - "Add URL" and "Remove URL" buttons
   - URL validation (format check, not accessibility yet)

3. Add document upload section:
   - File uploader accepting PDF, DOCX, TXT, MD
   - Multiple file support
   - Display uploaded file names and sizes
   - Clear uploaded files button

4. Add "Process Content" button (disabled if no inputs)

**Validation Criteria for Part 1A:**
- [ ] Can add/remove multiple URL input fields
- [ ] Can upload multiple documents simultaneously
- [ ] UI shows all uploaded files clearly
- [ ] Button enables only when inputs exist
- [ ] Session state preserves inputs

**Part 1B: Implement URL Content Extraction**
1. Create `utils/content_extractor.py`
2. Implement function `extract_from_url(url: str) -> dict`:
   - Use `trafilatura` for primary extraction
   - Fallback to `BeautifulSoup` if trafilatura fails
   - Return: `{"source": url, "title": str, "content": str, "word_count": int, "success": bool, "error": str}`

3. Add URL validation:
   - Check URL accessibility (HEAD request)
   - Handle timeouts gracefully
   - Return clear error messages

4. Test with various URLs:
   - Medium articles
   - News websites
   - Documentation pages

**Validation Criteria for Part 1B:**
- [ ] Successfully extracts content from 5 different URL types
- [ ] Handles invalid URLs without crashing
- [ ] Returns structured data with all required fields
- [ ] Error messages are user-friendly

**Part 1C: Implement Document Content Extraction**
1. Extend `utils/content_extractor.py`
2. Implement `extract_from_pdf(file) -> dict`
3. Implement `extract_from_docx(file) -> dict`
4. Implement `extract_from_text(file) -> dict`

**Validation Criteria for Part 1C:**
- [ ] Extracts text from PDF correctly
- [ ] Extracts text from DOCX with formatting preserved
- [ ] Handles TXT and MD files
- [ ] Returns consistent data structure

**Part 1D: Content Aggregation**
1. Implement `aggregate_content(sources: list[dict]) -> dict`:
   - Combine content from all sources
   - Maintain source attribution
   - Remove obvious duplicates
   - Calculate total word count
   - Validate 500-5,000 word range

2. Add error handling for:
   - No content extracted
   - Content too short (<500 words)
   - Content too long (>5,000 words)

**Validation Criteria for Part 1D:**
- [ ] Combines multiple sources correctly
- [ ] Preserves source attribution
- [ ] Word count validation works
- [ ] Clear error messages for edge cases

**Part 1E: Integration with Streamlit UI**
1. Connect extraction functions to "Process Content" button
2. Show progress bar during extraction
3. Display results:
   - Success/failure for each source
   - Total word count
   - Preview of combined content (first 500 chars)
   - Error messages for failed sources

4. Store extracted content in session state

**Validation Criteria for Part 1E:**
- [ ] Progress bar shows during processing
- [ ] Clear success/failure indicators
- [ ] Content preview displays correctly
- [ ] Session state maintains extracted content
- [ ] Can process 1 URL + 2 documents simultaneously

**COMPREHENSIVE STAGE 1 VALIDATION:**
Test the complete Stage 1 with:
1. Single URL input → Extract → Display
2. Multiple URLs → Extract → Combine → Display
3. Single document upload → Extract → Display
4. Multiple documents → Extract → Combine → Display
5. Mixed URLs + documents → Extract → Combine → Display
6. Invalid URL → Show error
7. Corrupted document → Show error
8. Empty inputs → Prevent processing

**DO NOT PROCEED TO STAGE 2 UNTIL ALL STAGE 1 VALIDATIONS PASS.**

---

### **STAGE 2: AI Script Generation** (Implement THIRD)

**Objective:** Generate podcast scripts from extracted content with 2-4 dynamic personas.

**AI Agent Tasks:**

**Part 2A: Persona Definition System**
1. Create `utils/script_generator.py`
2. Define persona profiles:
   ```python
   PERSONAS = {
       "host_a": {"name": "Alex", "style": "enthusiastic, curious"},
       "host_b": {"name": "Bailey", "style": "analytical, skeptical"},
       "host_c": {"name": "Casey", "style": "expert, technical"},
       "host_d": {"name": "Drew", "style": "devil's advocate"}
   }
   ```

3. Implement `determine_speaker_count(content_dict: dict) -> int`:
   - 2 speakers: <1000 words, simple topic
   - 3 speakers: 1000-3000 words, moderate complexity
   - 4 speakers: >3000 words, complex/multi-faceted

**Validation Criteria for Part 2A:**
- [ ] Persona definitions are clear and distinct
- [ ] Speaker count determination is logical
- [ ] Returns 2-4 speakers based on content

**Part 2B: Prompt Engineering**
1. Create system prompt template that:
   - Defines each persona's role
   - Specifies conversation structure
   - Sets target word count based on duration
   - Requires JSON output format

2. Implement duration-to-word-count mapping:
   - 2 minutes → 300-400 words
   - 3 minutes → 450-550 words
   - 5 minutes → 750-850 words

3. Create example conversations for few-shot learning

**Validation Criteria for Part 2B:**
- [ ] Prompt is clear and comprehensive
- [ ] Word count targets are appropriate
- [ ] JSON format is well-specified

**Part 2C: OpenAI Integration**
1. Implement `generate_script(content: dict, duration: int, num_speakers: int) -> dict`:
   - Call OpenAI API with structured prompt
   - **Use GPT-4o-mini for MVP** (cost-effective: ~$0.01 per script)
   - Can upgrade to GPT-4 later for better quality
   - Parse JSON response
   - Validate script structure

2. Response format:
   ```json
   {
     "title": "Episode Title",
     "speakers": ["Alex", "Bailey"],
     "duration_target": 2,
     "dialogue": [
       {"speaker": "Alex", "text": "Welcome to..."},
       {"speaker": "Bailey", "text": "Thanks Alex..."}
     ]
   }
   ```

3. Add error handling:
   - API failures
   - Invalid JSON
   - Missing required fields

**Validation Criteria for Part 2C:**
- [ ] API integration works
- [ ] Returns valid JSON structure
- [ ] Error handling is robust
- [ ] Response parsing is reliable

**Part 2D: Script Quality Validation**
1. Implement quality checks:
   - Balanced speaking time (no speaker >60% of dialogue)
   - Minimum turns per speaker (at least 3)
   - Natural conversation flow (alternating speakers mostly)
   - Word count within target range (±10%)

2. Add regeneration logic if quality checks fail

**Validation Criteria for Part 2D:**
- [ ] Quality checks identify poor scripts
- [ ] Regeneration improves quality
- [ ] Maximum 3 regeneration attempts

**Part 2E: Integration with Streamlit**
1. Add "Generate Script" button (after content extraction)
2. Show progress during generation
3. Display generated script:
   - Formatted dialogue view
   - Speaker color coding
   - Word count and estimated duration

4. Store script in session state

**Validation Criteria for Part 2E:**
- [ ] Script generation triggered correctly
- [ ] Progress indication works
- [ ] Script displays beautifully
- [ ] Session state maintains script

**COMPREHENSIVE STAGE 2 VALIDATION:**
Test with:
1. Short content (500 words) → 2 speakers, 2 min
2. Medium content (2000 words) → 3 speakers, 3 min
3. Long content (4000 words) → 4 speakers, 5 min
4. Technical content → Validates expert persona usage
5. Simple content → Validates basic 2-speaker format

**DO NOT PROCEED TO STAGE 3 UNTIL ALL STAGE 2 VALIDATIONS PASS.**

---

### **STAGE 3: Text-to-Speech Audio Synthesis** (Implement FOURTH)

**Objective:** Convert script to audio using TTS with distinct voices.

**AI Agent Tasks:**

**Part 3A: Voice Profile Assignment**
1. Create `utils/audio_synthesizer.py`
2. Define voice mappings (OpenAI TTS):
   ```python
   VOICE_PROFILES = {
       "Alex": "alloy",    # Enthusiastic
       "Bailey": "echo",   # Analytical
       "Casey": "fable",   # Expert
       "Drew": "onyx"      # Skeptical
   }
   ```

3. Implement `assign_voices(speakers: list) -> dict`

**Validation Criteria for Part 3A:**
- [ ] Each speaker gets unique voice
- [ ] Voice assignment is consistent

**Part 3B: TTS API Integration**
1. Implement `synthesize_speech(text: str, voice: str) -> bytes`:
   - Call OpenAI TTS API
   - Return audio bytes
   - Handle API errors

2. Add rate limiting:
   - Max 10 concurrent requests
   - Respect API limits

**Validation Criteria for Part 3B:**
- [ ] Single text-to-speech works
- [ ] Voice parameter changes output
- [ ] Error handling functions

**Part 3C: Parallel Processing**
1. Implement `batch_synthesize(dialogue: list, voice_map: dict) -> list`:
   - Process multiple segments in parallel
   - Use ThreadPoolExecutor
   - Track progress

2. Save temporary audio files:
   - Format: `temp/segment_{index}_{speaker}.mp3`
   - Clean up on completion

**Validation Criteria for Part 3C:**
- [ ] Parallel processing works
- [ ] All segments generated
- [ ] Temporary files created correctly
- [ ] Progress tracking functional

**Part 3D: Integration with Streamlit**
1. Add "Generate Audio" button (after script generation)
2. Show detailed progress:
   - "Synthesizing segment X of Y"
   - Progress bar
   - ETA calculation

3. Display completion message with file count

**Validation Criteria for Part 3D:**
- [ ] Audio generation triggers correctly
- [ ] Progress updates in real-time
- [ ] Completion message shows

**COMPREHENSIVE STAGE 3 VALIDATION:**
Test with:
1. 2-speaker script → 2 distinct voices
2. 4-speaker script → 4 distinct voices
3. Long script (30+ segments) → All segments created
4. API failure simulation → Error handling

**DO NOT PROCEED TO STAGE 4 UNTIL ALL STAGE 3 VALIDATIONS PASS.**

---

### **STAGE 4: Audio Post-Processing & Assembly** (Implement FIFTH)

**Objective:** Stitch audio segments into final podcast with crossfades and normalization.

**AI Agent Tasks:**

**Part 4A: FFmpeg Integration**
1. Create `utils/audio_processor.py`
2. Verify FFmpeg installation
3. Implement `concatenate_audio(segments: list, output_path: str)`:
   - Use pydub for Python-based audio processing
   - Alternative: subprocess calls to FFmpeg

**Validation Criteria for Part 4A:**
- [ ] FFmpeg available or pydub works
- [ ] Basic concatenation functions

**Part 4B: Crossfade Implementation**
1. Implement `apply_crossfade(audio1, audio2, duration_ms=100)`:
   - Use pydub crossfade
   - 50-100ms fade duration

2. Apply to all segment transitions

**Validation Criteria for Part 4B:**
- [ ] Crossfades sound natural
- [ ] No audio pops or clicks

**Part 4C: Audio Normalization**
1. Implement `normalize_audio(audio) -> audio`:
   - Balance levels across segments
   - Use pydub normalize()

2. Apply to final concatenated audio

**Validation Criteria for Part 4C:**
- [ ] Audio levels consistent
- [ ] No distortion from normalization

**Part 4D: Final Assembly**
1. Implement `create_podcast(segments: list, output_file: str) -> str`:
   - Load all segments
   - Apply crossfades between segments
   - Normalize final audio
   - Export as MP3 (192 kbps)

2. Clean up temporary files

**Validation Criteria for Part 4D:**
- [ ] Final MP3 created
- [ ] Audio quality is high
- [ ] File size reasonable
- [ ] Temp files deleted

**Part 4E: Integration with Streamlit**
1. Add "Create Final Podcast" button
2. Show processing progress
3. Display:
   - Audio player with final podcast
   - Download button
   - File size and duration info

4. Store final file path in session state

**Validation Criteria for Part 4E:**
- [ ] Final processing triggered correctly
- [ ] Audio player works
- [ ] Download button functions
- [ ] File info displayed

**COMPREHENSIVE STAGE 4 VALIDATION:**
Test with:
1. 2-minute podcast → Clean output
2. 5-minute podcast → Clean output
3. Multiple speaker podcast → Smooth transitions
4. Listen for audio quality issues

**DO NOT PROCEED TO STAGE 5 UNTIL ALL STAGE 4 VALIDATIONS PASS.**

---

### **STAGE 5: End-to-End Integration & Testing** (Implement LAST)

**Objective:** Complete full pipeline integration and comprehensive testing.

**AI Agent Tasks:**

**Part 5A: Full Pipeline Integration**
1. Create workflow orchestrator in `app.py`
2. Implement `process_full_pipeline()`:
   - Stage 1: Extract content
   - Stage 2: Generate script
   - Stage 3: Synthesize audio
   - Stage 4: Create final podcast

3. Add overall progress tracking across all stages

**Part 5B: Error Recovery**
1. Implement checkpointing:
   - Save progress after each stage
   - Allow resume from checkpoint

2. Add retry logic for API failures

**Part 5C: Comprehensive Testing**
1. Test all combinations:
   - URL only
   - Document only
   - Multiple URLs
   - Multiple documents
   - Mixed sources

2. Test all durations (2, 3, 5 minutes)
3. Test all speaker counts (2, 3, 4)

**Part 5D: UI Polish**
1. Add clear instructions
2. Improve error messages
3. Add example inputs
4. Add FAQ section

**FINAL VALIDATION:**
- [ ] Complete pipeline works end-to-end
- [ ] All edge cases handled
- [ ] Error messages are helpful
- [ ] UI is intuitive
- [ ] Documentation is complete

---

### AI Agent Self-Check Questions

Before marking any stage as complete, the AI agent must answer:

1. ✅ Have I implemented ALL parts of this stage?
2. ✅ Have I tested EACH validation criteria?
3. ✅ Have I documented my code with comments?
4. ✅ Have I handled errors gracefully?
5. ✅ Can I demonstrate this stage working independently?
6. ✅ Is the code maintainable and following best practices?

**If ANY answer is NO, the stage is NOT complete.**

---

### Communication Protocol for AI Agent

When implementing, the AI agent should:

1. **Before starting each stage:** 
   - Confirm understanding of objectives
   - List all tasks to be completed
   - Estimate completion approach

2. **During implementation:**
   - Show code being written
   - Explain key decisions
   - Flag potential issues proactively

3. **After completing each part:**
   - Run validation checks
   - Show test results
   - Confirm readiness for next part

4. **When encountering issues:**
   - Clearly describe the problem
   - Propose 2-3 solution approaches
   - Ask for guidance if needed

5. **After completing each stage:**
   - Summarize what was accomplished
   - Confirm all validations passed
   - Request permission to proceed to next stage

---

10\. Development Roadmap

**Note:** The roadmap below has been superseded by the detailed stage-by-stage implementation guide in Section 9.4. Follow that guide for actual development.

10.1 Revised MVP Timeline (Stage-Based)

**Week 1-2: Foundation & Infrastructure**

-   Set up development environment and project structure

-   Implement basic frontend with URL input and progress display

-   Set up backend API framework and task queue

-   Integrate web scraping and content extraction

**Week 3-4: Core AI Pipeline**

-   Develop and test LLM prompt for script generation

-   Integrate TTS API with parallel processing

-   Implement script parser and validation

-   Build audio stitching pipeline with FFmpeg

**Week 5-6: Polish & Testing**

-   Add audio player and download functionality

-   Implement comprehensive error handling

-   Performance optimization and latency reduction

-   End-to-end testing with various content types

-   Deploy to production environment

10.2 Phase 2: Enhancement (Weeks 7-10)

-   Add custom persona selection

-   Implement adjustable podcast length

-   Enhance UI/UX based on user feedback

-   Add analytics and usage tracking

-   Implement caching for improved performance

10.3 Phase 3: Scale (Weeks 11-14)

-   Add user accounts and authentication

-   Build podcast library and history

-   Implement RSS feed generation

-   Develop browser extension

-   Add social sharing features

---

## 10.4 Free Hosting Strategy

### MVP Demo (Week 1-2)
**Goal:** Get working demo running locally for testing and iteration

**Setup:**
- Run on local machine: `streamlit run app.py`
- Access at `http://localhost:8501`
- No hosting costs
- Fast iteration and debugging

### Public Demo (Week 3-4)
**Goal:** Share demo with users for feedback

**Option 1: Streamlit Community Cloud (Recommended for MVP)**
- **Cost:** 100% Free
- **Limits:** 1GB RAM, public repos only
- **Pros:** Zero setup, deploy from GitHub
- **Cons:** Limited resources, app sleeps after inactivity
- **Setup:**
  1. Push code to GitHub
  2. Connect at share.streamlit.io
  3. Deploy in one click
- **Best for:** Quick demos, getting user feedback

**Option 2: Hugging Face Spaces**
- **Cost:** Free tier available
- **Limits:** 16GB RAM, 2 CPU cores
- **Pros:** More resources, persistent, supports Streamlit
- **Cons:** Slightly more complex setup
- **Setup:**
  1. Create Space on huggingface.co
  2. Choose Streamlit SDK
  3. Push code to Space repo
- **Best for:** Better performance, more professional demo

### Production Hosting (Post-MVP)

**Backend Options (Free Tier):**

1. **Render (Recommended)**
   - **Free Tier:** 750 hours/month
   - **Limits:** Sleeps after 15 min inactivity, 512MB RAM
   - **Pros:** Easy setup, auto-deploy from GitHub
   - **Cons:** Cold starts (15-30s wake time)
   - **Best for:** API backend

2. **Railway**
   - **Free Tier:** $5 credit/month, then pay-as-you-go
   - **Limits:** Credit-based
   - **Pros:** No sleep, better performance
   - **Cons:** Limited free credits
   - **Best for:** Critical services needing 24/7 uptime

3. **Fly.io**
   - **Free Tier:** 3 shared-CPU VMs, 3GB storage
   - **Limits:** Shared resources
   - **Pros:** Global edge deployment, no sleep
   - **Cons:** More complex setup
   - **Best for:** Low-latency global access

**Frontend Options (Free Tier):**

1. **Vercel (Recommended)**
   - **Free Tier:** 100GB bandwidth, unlimited sites
   - **Limits:** Bandwidth cap
   - **Pros:** Amazing DX, fast deployment, edge network
   - **Cons:** None for our use case
   - **Best for:** Next.js/React frontend

2. **Netlify**
   - **Free Tier:** 100GB bandwidth, 300 build minutes
   - **Limits:** Similar to Vercel
   - **Pros:** Great for static sites
   - **Cons:** Slightly slower than Vercel
   - **Best for:** Alternative to Vercel

**Storage Options (Free Tier):**

1. **Cloudflare R2**
   - **Free Tier:** 10GB storage, 1M writes/month
   - **Limits:** Good for MVP
   - **Pros:** No egress fees, fast
   - **Cons:** Requires Cloudflare account
   - **Best for:** Audio file storage

2. **Supabase Storage**
   - **Free Tier:** 1GB storage
   - **Limits:** Smaller than R2
   - **Pros:** Includes database, authentication
   - **Cons:** 1GB might fill up quickly
   - **Best for:** All-in-one solution

**Recommended Free Stack:**

```
┌─────────────────────────────────────────┐
│  Frontend: Vercel (Next.js + Tailwind) │
│  - Free: 100GB bandwidth               │
│  - Deploy from GitHub                  │
└─────────────────────────────────────────┘
              ↓ API calls
┌─────────────────────────────────────────┐
│  Backend: Render (FastAPI)             │
│  - Free: 750 hours/month               │
│  - Sleeps after 15 min (cold start)    │
└─────────────────────────────────────────┘
              ↓ saves to
┌─────────────────────────────────────────┐
│  Storage: Cloudflare R2                │
│  - Free: 10GB + 1M operations          │
│  - CDN delivery for audio files        │
└─────────────────────────────────────────┘
```

**Cost Optimization Tips:**

1. **Cache aggressively:**
   - Cache script generation for identical content
   - Store generated podcasts for 7 days
   - Reduces API calls to OpenAI

2. **Use GPT-4o-mini instead of GPT-4:**
   - 60x cheaper ($0.15/1M → $0.0025/1M tokens)
   - Good enough quality for MVP
   - Can upgrade later

3. **Optimize TTS usage:**
   - OpenAI TTS: $15/1M characters
   - 2-min podcast ≈ 400 words ≈ 2000 chars = $0.03
   - Cache by content hash to avoid regeneration

4. **Handle cold starts:**
   - Keep backend "warm" with cron job (free)
   - Use Vercel Edge Functions for instant response
   - Show "waking up" message to users

5. **Monitor usage:**
   - Set up OpenAI usage alerts
   - Track R2 storage usage
   - Implement rate limiting

**Free Tier Limits (Monthly):**

| Service | Free Limit | Cost if Exceeded |
|---------|-----------|------------------|
| Render Backend | 750 hours | Upgrade to $7/mo |
| Vercel Frontend | 100GB bandwidth | $20/100GB |
| Cloudflare R2 | 10GB storage | $0.015/GB |
| OpenAI GPT-4o-mini | Pay-as-you-go | $0.15/1M input tokens |
| OpenAI TTS | Pay-as-you-go | $15/1M characters |

**Expected Costs (100 podcasts/month):**
- Script generation: 100 × $0.02 = $2.00
- TTS synthesis: 100 × $0.03 = $3.00
- Storage: Free (< 1GB)
- Hosting: Free (within limits)
- **Total: ~$5/month** for 100 podcasts

**Scaling Path:**

1. **0-100 users:** Free tier everything
2. **100-1000 users:** Upgrade Render ($7/mo), add Redis cache
3. **1000+ users:** Consider dedicated hosting, optimize costs

11\. Risk Assessment

  -------------------------------------------- ----------------- ----------------- --------------------------------------------------------------------------
  **Risk**                                     **Impact**        **Probability**   **Mitigation**

  High API costs from TTS/LLM usage            High              Medium            Implement caching, usage quotas, and cost monitoring

  Poor script quality from LLM                 High              Medium            Extensive prompt engineering, quality validation, regeneration fallbacks

  Processing timeouts and failures             Medium            High              Robust retry logic, graceful degradation, clear error messages

  Content extraction failures                  Medium            High              Multiple extraction strategies, manual text paste fallback

  Scalability bottlenecks                      Medium            Low               Design for horizontal scaling from start, load testing

  Copyright/legal issues with source content   High              Low               Clear ToS, user-generated content model, legal review
  -------------------------------------------- ----------------- ----------------- --------------------------------------------------------------------------

12\. Open Questions & Decisions Needed

-   Which TTS provider offers best quality-to-cost ratio: OpenAI TTS, ElevenLabs, Google Cloud TTS, or AWS Polly?

-   Should we support multiple languages in MVP or English-only initially?

-   What monetization model: freemium with usage limits, subscription, or pay-per-podcast?

-   How to handle paywalled content - skip entirely or allow API key integration?

-   Should generated podcasts be publicly shareable or user-private by default?

-   What retention policy for generated audio files: 24 hours, 7 days, or permanent storage?

-   Do we need content moderation for generated podcasts to prevent misuse?

13\. Appendices

13.1 Example Prompt for Script Generation

**System Prompt:**

*You are an expert podcast script writer. Create an engaging 5-minute conversational podcast script between two hosts discussing the provided article. Host A (Alex) is enthusiastic and curious, asking clarifying questions. Host B (Bailey) is more analytical and skeptical, providing counterpoints and deeper analysis. The conversation should feel natural with interruptions, agreements, and smooth transitions. Structure: 1) Brief intro mentioning article title/source, 2) Discussion of 3-4 key points, 3) Implications and analysis, 4) Conclusion with takeaways. Output in JSON format with speaker labels.*

13.2 Example FFmpeg Command

*ffmpeg -i segment1.mp3 -i segment2.mp3 -filter_complex \"\[0\]afade=t=out:st=2.9:d=0.1\[a0\];\[1\]afade=t=in:st=0:d=0.1\[a1\];\[a0\]\[a1\]concat=n=2:v=0:a=1,loudnorm\" -b:a 192k output.mp3*

13.3 Cost Estimates (Per Podcast)

**MVP Pricing (Using GPT-4o-mini for cost efficiency):**

  ---------------------------------------------- ----------------- -----------------
  **Component**                                  **Provider**      **Est. Cost**

  Script Generation (GPT-4o-mini, \~2K tokens)   OpenAI            \$0.01

  TTS Synthesis (\~400 words for 2-min)          OpenAI TTS        \$0.03

  Compute & Storage (local/free tier)            Free              \$0.00

  **Total per 2-min Podcast**                                      **\$0.04**
  ---------------------------------------------- ----------------- -----------------

**Production Pricing (Upgrading to GPT-4 for better quality):**

  ---------------------------------------------- ----------------- -----------------
  **Component**                                  **Provider**      **Est. Cost**

  Script Generation (GPT-4 Turbo, \~2K tokens)   OpenAI            \$0.02

  TTS Synthesis (\~800 words for 5-min)          OpenAI TTS        \$0.12

  Hosting & Storage                              Free tier         \$0.00

  **Total per 5-min Podcast**                                      **\$0.14**
  ---------------------------------------------- ----------------- -----------------

**Monthly Costs (100 podcasts):**
- MVP (2-min, GPT-4o-mini): $4/month
- Production (5-min, GPT-4): $14/month

All hosting remains free within tier limits.

*\-\-- End of Document \-\--*
