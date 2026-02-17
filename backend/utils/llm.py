import os
import gc
import subprocess
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel, pipeline
from huggingface_hub import login
from dotenv import load_dotenv
from groq import Groq
from google import genai
from openai import OpenAI

load_dotenv()

# ... existing constants ...
PROVIDER_OPENAI = "OpenAI"
PROVIDER_GEMINI = "Gemini"
PROVIDER_LOCAL = "Local LLM"
PROVIDER_GROQ = "Groq"

MODEL_GEMINI_FLASH = "gemini-3-flash-preview"
MODEL_GEMINI_PRO = "gemini-3-pro-preview"

GEMINI_MODELS = [MODEL_GEMINI_FLASH, MODEL_GEMINI_PRO]

MODEL_GROQ_LLAMA_3_1_8B_INSTANT = "llama-3.1-8b-instant"

MODEL_LOCAL_3B = "meta-llama/Llama-3.2-3B-Instruct"
MODEL_LOCAL_1B = "meta-llama/Llama-3.2-1B-Instruct"
MODEL_LOCAL_QWEN_1_5B = "MaziyarPanahi/Qwen2-1.5B-Instruct-GGUF"

# Global cache
_LOCAL_PIPELINE = None
_LOADED_MODEL_ID = None

def get_local_model_pipeline(model_id):
    """Loads a local model pipeline efficiently."""
    global _LOCAL_PIPELINE, _LOADED_MODEL_ID
    
    if _LOCAL_PIPELINE is not None and _LOADED_MODEL_ID == model_id:
        return _LOCAL_PIPELINE

    try:
        # Authenticate with Hugging Face if token is present
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            login(token=hf_token)
        
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        if "GGUF" in model_id:
            # Load model directly as requested for GGUF
            model = AutoModel.from_pretrained(model_id, dtype="auto")
        else:
            # dynamic device map and quantization for standard models
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16,
                device_map="auto",
            )
        
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=2048,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True,
        )
        
        _LOCAL_PIPELINE = pipe
        _LOADED_MODEL_ID = model_id
        return pipe
    except Exception as e:
        print(f"Error loading local model {model_id}: {e}")
        return None

def unload_local_model():
    """Unloads the local model from memory and clears CUDA cache."""
    global _LOCAL_PIPELINE, _LOADED_MODEL_ID
    
    _LOCAL_PIPELINE = None
    _LOADED_MODEL_ID = None
    
    # Force garbage collection
    gc.collect()
    
    # Clear CUDA cache if applicable
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    print("Local LLM unloaded to free up memory for TTS.")
    
    # Run nvidia-smi to check VRAM
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error running nvidia-smi: {result.stderr}"
    except Exception as e:
        return f"Failed to run nvidia-smi: {e}"

def query_llm(messages: list[dict], provider: str, model_name: str, api_key: str = None, local_pipeline = None) -> str:
# ... rest of the file ...

    """Unified interface for querying LLMs."""
    
    if provider == PROVIDER_OPENAI:
        if not api_key:
            raise ValueError("OpenAI API Key is required.")
        
        client = OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API Error: {str(e)}")

    elif provider == PROVIDER_GEMINI:
        if not api_key:
            raise ValueError("Gemini API Key is required.")
        
        try:
            client = genai.Client(api_key=api_key)
            
            # Convert messages to Gemini format (simplified)
            # Assuming last message is user prompt, previous are history/system
            user_message = messages[-1]['content']
            system_instruction = next((m['content'] for m in messages if m['role'] == 'system'), None)

            # Construct config if system instruction exists
            config = None
            if system_instruction:
                 # system_instruction is passed directly to generate_content in newer SDKs or client init?
                 # Based on test.py, it's just client.models.generate_content
                 # We might need to handle system instructions differently or check SDK docs.
                 # safe bet: prepend system instruction to user message for now if SDK is very new,
                 # OR try to find if generate_content supports system_instruction.
                 # Re-reading test.py: it just uses contents="...".
                 # Let's check if we can pass system_instruction to generate_content or client.
                 # The previous implementation used system_instruction in GenerativeModel.
                 # The new SDK `google-genai` (v1/v2?) often uses `config` or similar.
                 # detailed check: `test.py` uses `client.models.generate_content(..., contents=...)`.
                 # Let's assumes we just pass the user message for now, or prepend system prompt.
                 # Actually, looking at commonly available `google-genai` usage:
                 # It supports `config=types.GenerateContentConfig(system_instruction=...)`
                 # specific imports might be needed: `from google.genai import types`
                 pass

            # Update: To be safe and follow `test.py` simplicity which didn't show system prompt usage,
            # but we need it.
            # Let's try to pass `config` if we can import types, or just prepend.
            # simpler approach: just formatting the content.
            
            final_content = user_message
            if system_instruction:
                final_content = f"System Instruction: {system_instruction}\n\nUser Question: {user_message}"

            response = client.models.generate_content(
                model=model_name,
                contents=final_content
            )
            return response.text
        except Exception as e:
             raise Exception(f"Gemini API Error: {str(e)}")

    elif provider == PROVIDER_LOCAL:
        if not local_pipeline:
             # Fallback to global pipeline
             if _LOCAL_PIPELINE:
                 local_pipeline = _LOCAL_PIPELINE
             else:
                 raise ValueError("Local model pipeline not initialized.")
        
        try:
            outputs = local_pipeline(
                messages,
                max_new_tokens=4096,
            )
            return outputs[0]["generated_text"][-1]["content"]
        except Exception as e:
             raise Exception(f"Local Model Error: {str(e)}")

    elif provider == PROVIDER_GROQ:
        if not api_key:
            raise ValueError("Groq API Key is required.")
        
        client = Groq(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
                stop=None
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API Error: {str(e)}")
    
    else:
        raise ValueError(f"Unknown provider: {provider}")
