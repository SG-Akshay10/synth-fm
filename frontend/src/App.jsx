import { useState } from 'react'
import axios from 'axios'
import { AppLayout } from './components/layout/AppLayout'
import { ContentInput } from './components/features/ContentInput'
import { ScriptReview } from './components/features/ScriptReview'
import { AudioPlayer } from './components/features/AudioPlayer'
import { Loader2 } from 'lucide-react'

const API_BASE_URL = "http://localhost:8000/api"

function App() {
  // Configuration State
  const [config, setConfig] = useState({
    provider: "local",
    apiKey: "",
    modelName: "local_3b",
    duration: 2,
    numSpeakers: 2,
    podcastName: "Synth-FM",
    speakers: [
      { name: "Alex", gender: "Female" },
      { name: "Bailey", gender: "Male" }
    ]
  })

  // Content State
  const [urls, setUrls] = useState([""])
  const [files, setFiles] = useState([])
  const [extractedContent, setExtractedContent] = useState(null)

  // Script & Audio State
  const [script, setScript] = useState(null)
  const [audioSegments, setAudioSegments] = useState([])
  const [finalAudioPath, setFinalAudioPath] = useState(null)

  // UI State
  const [loading, setLoading] = useState(false)
  const [modelLoading, setModelLoading] = useState(false)
  const [modelLoaded, setModelLoaded] = useState(false)
  const [statusMessage, setStatusMessage] = useState("")

  // Handlers
  const handleLoadModel = async () => {
    setModelLoading(true)
    setStatusMessage(`Loading model ${config.modelName}...`)
    try {
      await axios.post(`${API_BASE_URL}/model/load`, { model_name: config.modelName })
      setModelLoaded(true)
      setStatusMessage(`Model ${config.modelName} loaded!`)
    } catch (error) {
      console.error(error)
      setStatusMessage(`Error loading model: ${error.message}`)
    } finally {
      setModelLoading(false)
    }
  }

  const handleUnloadModel = async () => {
    setLoading(true)
    setStatusMessage("Unloading model...")
    try {
      await axios.post(`${API_BASE_URL}/model/unload`)
      setModelLoaded(false)
      setStatusMessage("Model unloaded!")
    } catch (error) {
      console.error(error)
      setStatusMessage(`Error unloading model: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleUrlChange = (index, value) => {
    const newUrls = [...urls]
    newUrls[index] = value
    setUrls(newUrls)
  }

  const handleAddUrl = () => setUrls([...urls, ""])
  const handleRemoveUrl = (index) => setUrls(urls.filter((_, i) => i !== index))

  const handleFileChange = (e) => setFiles([...e.target.files])

  // API Interactions
  const processContent = async () => {
    setLoading(true)
    setStatusMessage("Extracting content...")
    try {
      let aggregatedContent = []

      // Extract URLs
      const validUrls = urls.filter(u => u.trim())
      if (validUrls.length > 0) {
        const res = await axios.post(`${API_BASE_URL}/content/extract-urls`, { urls: validUrls })
        if (res.data.valid) aggregatedContent.push(res.data)
      }

      // Extract Files
      if (files.length > 0) {
        const formData = new FormData()
        files.forEach(file => formData.append('files', file))
        const res = await axios.post(`${API_BASE_URL}/content/extract-files`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        if (res.data.valid) aggregatedContent.push(res.data)
      }

      if (aggregatedContent.length > 0) {
        // Just taking the last one for now to keep it simple, or merging if multiple
        const final = aggregatedContent[aggregatedContent.length - 1]
        setExtractedContent(final)
        setStatusMessage("Content extracted!")
      } else {
        setStatusMessage("No valid content found.")
      }

    } catch (error) {
      console.error(error)
      setStatusMessage(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const generateScript = async () => {
    if (!extractedContent) return
    setLoading(true)
    setStatusMessage("Generating script...")
    try {
      const res = await axios.post(`${API_BASE_URL}/script/generate-script`, {
        content: extractedContent.combined_content,
        duration: config.duration,
        num_speakers: config.numSpeakers,
        podcast_name: config.podcastName,
        speaker_names: config.speakers.map(s => s.name),
        provider: config.provider,
        api_key: config.apiKey,
        model_name: config.modelName
      })
      setScript(res.data)
      setStatusMessage("Script generated!")
    } catch (error) {
      console.error(error)
      setStatusMessage(`Error generating script: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const synthesizeAudio = async () => {
    if (!script) return
    setLoading(true)
    setStatusMessage("Synthesizing audio (this may take a while)...")
    try {
      const speakerGenders = {}
      config.speakers.forEach(s => speakerGenders[s.name] = s.gender)

      const res = await axios.post(`${API_BASE_URL}/audio/synthesize-audio`, {
        script: script,
        speaker_names: config.speakers.map(s => s.name),
        speaker_genders: speakerGenders,
        provider: "local"
      })
      setAudioSegments(res.data.audio_paths)
      setStatusMessage("Audio segments created!")

      // Auto create final podcast
      setStatusMessage("Stitching final podcast...")
      const finalRes = await axios.post(`${API_BASE_URL}/audio/create-podcast`, {
        audio_paths: res.data.audio_paths
      })
      setFinalAudioPath(finalRes.data.final_audio_path)
      setStatusMessage("Podcast ready!")

    } catch (error) {
      console.error(error)
      setStatusMessage(`Error synthesizing audio: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <AppLayout
      config={config}
      onConfigChange={setConfig}
      onLoadModel={handleLoadModel}
      onUnloadModel={handleUnloadModel}
      modelLoading={modelLoading}
      modelLoaded={modelLoaded}
    >
      <header className="flex justify-between items-center pb-6 border-b border-white/5">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">
            {config.podcastName}
          </h1>
          <p className="text-gray-400 text-sm mt-1">Create studio-quality podcasts with AI</p>
        </div>

        {loading && (
          <div className="flex items-center gap-3 bg-violet-500/10 px-4 py-2 rounded-full border border-violet-500/20">
            <Loader2 className="animate-spin text-violet-400" size={18} />
            <span className="text-sm font-medium text-violet-300 animate-pulse">
              {statusMessage || "Processing..."}
            </span>
          </div>
        )}
      </header>

      <div className="space-y-12">
        <section className="animate-in fade-in slide-in-from-bottom-4 duration-500">
          <ContentInput
            urls={urls}
            onUrlChange={handleUrlChange}
            onAddUrl={handleAddUrl}
            onRemoveUrl={handleRemoveUrl}
            files={files}
            onFileChange={handleFileChange}
            onProcess={processContent}
            loading={loading}
          />
        </section>

        {(extractedContent || script) && (
          <section className="animate-in fade-in slide-in-from-bottom-8 duration-700">
            <ScriptReview
              content={extractedContent}
              script={script}
              onGenerateScript={generateScript}
              onSynthesize={synthesizeAudio}
              loading={loading}
              speakers={config.speakers}
            />
          </section>
        )}
      </div>

      {finalAudioPath && (
        <AudioPlayer audioPath={finalAudioPath} />
      )}
    </AppLayout>
  )
}

export default App
