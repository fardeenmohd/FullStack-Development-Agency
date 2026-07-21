import requests
import json
import time
import sys

# Ollama runs locally on port 11434 by default
OLLAMA_URL = "http://localhost:11434/api/generate"
# The specific coding model we pulled for your 8GB VRAM
LOCAL_MODEL = "qwen2.5-coder:7b"

def generate_local_code(system_prompt: str, user_content: str) -> dict:
    """
    Routes the prompt to the local 3070 Ti via Ollama and returns clean JSON.
    """
    payload = {
        "model": LOCAL_MODEL,
        "prompt": user_content,
        "system": system_prompt,
        "stream": False,
        "format": "json", # Ollama natively supports forcing JSON output
        "options": {
            "temperature": 0.1,
            "num_predict": 8000 # Increased to 8000 to prevent JSON truncation
        }
    }

    print(f"⚙️  Spinning up 3070 Ti ({LOCAL_MODEL})...")
    start_time = time.time()
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300) # 5 min timeout for heavy generation
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error from Ollama: {e}")
        print(f"Ollama response details: {response.text}")
        print(f"\n💡 Hint: Run 'ollama list' in your terminal to see your downloaded models.")
        print(f"If your model is named something else (like 'qwen2.5-coder:latest'), update the LOCAL_MODEL variable at the top of this script!")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Ollama. Is the Ollama app running on your machine?")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during local generation: {e}")
        sys.exit(1)
        
    result_text = response.json().get("response", "")
    print(f"⏱️  Local generation took {round(time.time() - start_time, 2)} seconds.")
    
    # Strip markdown backticks just in case the model hallucinates them despite format: json
    raw_text = result_text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    elif raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]

    try:
        parsed_json = json.loads(raw_text.strip())
        return parsed_json
    except json.JSONDecodeError:
        print("❌ Error: Local model failed to return valid JSON. Raw output:")
        print(result_text)
        sys.exit(1)