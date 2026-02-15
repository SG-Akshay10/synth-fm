import os
import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login

# Constants
PROVIDER_OPENAI = "OpenAI"
PROVIDER_GEMINI = "Gemini"
PROVIDER_LOCAL = "Local LLM"

MODEL_GEMINI_FLASH = "gemini-1.5-flash"
MODEL_GEMINI_PRO = "gemini-1.5-pro"

MODEL_LOCAL_3B = "meta-llama/Llama-3.2-3B-Instruct"
MODEL_LOCAL_1B = "meta-llama/Llama-3.2-1B-Instruct"

@st.cache_resource
def get_local_model_pipeline(model_id):
    """Loads a local model pipeline efficiently."""
    try:
        # Authenticate with Hugging Face if token is present
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            login(token=hf_token)
        
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        # dynamic device map and quantization
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
        return pipe
    except Exception as e:
        st.error(f"Error loading local model {model_id}: {e}")
        return None

def query_llm(messages: list[dict], provider: str, model_name: str, api_key: str = None, local_pipeline = None) -> str:
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
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            
            # Convert messages to Gemini format (simplified)
            # Assuming last message is user prompt, previous are history/system
            # Gemini Python SDK handles history differently, but for 1-shot generation:
            user_message = messages[-1]['content']
            system_instruction = next((m['content'] for m in messages if m['role'] == 'system'), None)
            
            if system_instruction:
                model = genai.GenerativeModel(model_name, system_instruction=system_instruction)
            
            response = model.generate_content(user_message)
            return response.text
        except Exception as e:
             raise Exception(f"Gemini API Error: {str(e)}")

    elif provider == PROVIDER_LOCAL:
        if not local_pipeline:
             raise ValueError("Local model pipeline not initialized.")
        
        try:
            outputs = local_pipeline(
                messages,
                max_new_tokens=4096,
            )
            return outputs[0]["generated_text"][-1]["content"]
        except Exception as e:
             raise Exception(f"Local Model Error: {str(e)}")
    
    else:
        raise ValueError(f"Unknown provider: {provider}")
