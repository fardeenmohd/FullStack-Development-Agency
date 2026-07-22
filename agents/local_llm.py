import requests
import json
import time
import sys
from agency_utils import clean_llm_output

# Ollama runs locally on port 11434 by default
OLLAMA_URL = "http://localhost:11434/api/generate"
# The specific coding model we pulled for your 8GB VRAM
LOCAL_MODEL = "qwen2.5-coder:7b"
MAX_RETRIES = 3

def generate_local_code(system_prompt: str, user_content: str, expect_json: bool = True) -> dict | str:
    """
    Routes the prompt to the local 3070 Ti via Ollama. 
    Includes auto-retries for JSON parsing failures.
    """
    payload = {
        "model": LOCAL_MODEL,
        "prompt": user_content,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 8000
        }
    }
    
    if expect_json:
        payload["format"] = "json"

    print(f"⚙️  Spinning up 3070 Ti ({LOCAL_MODEL})...")
    
    for attempt in range(1, MAX_RETRIES + 1):
        start_time = time.time()
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=300)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to Ollama. Is the Ollama app running?")
            sys.exit(1)
        except Exception as e:
            print(f"❌ HTTP Error from Ollama: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2)
                continue
            sys.exit(1)
            
        result_text = response.json().get("response", "")
        print(f"⏱️  Local generation took {round(time.time() - start_time, 2)}s (Attempt {attempt}).")
        
        # Centralized cleanup of hallucinated markdown backticks
        raw_text = clean_llm_output(result_text)

        if not expect_json:
            return raw_text

        try:
            parsed_json = json.loads(raw_text)
            return parsed_json
        except json.JSONDecodeError:
            print(f"⚠️  JSON parsing failed on attempt {attempt}. Retrying...")
            if attempt == MAX_RETRIES:
                print("❌ Fatal: Local model failed to return valid JSON after max retries. Raw output:")
                print(result_text)
                sys.exit(1)
            time.sleep(1)