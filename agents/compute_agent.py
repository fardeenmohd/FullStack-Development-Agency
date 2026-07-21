import os
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

# Define the Compute Scientist's Persona and Rules
compute_persona = """
You are an expert Backend Engineer specializing in Python, FastAPI, and data engineering.
Your job is to read specific development instructions and generate high-performance microservices.

You must follow modern Python best practices:
- Use asynchronous endpoint definitions (async/await) for I/O operations.
- Include explicit Pydantic schemas for data validation.
- Enforce strict type hinting throughout the codebase.

You MUST output a strictly formatted JSON object containing:
1. "files": An array of objects, where each object has:
   - "path": The target filename/filepath (e.g., "main.py" or "schemas.py")
   - "code": The full, un-truncated string content of the python code file.
"""

def run_compute_agent(instruction_path: str):
    if not os.path.exists(instruction_path):
        print(f"❌ Error: {instruction_path} not found. Run synthesizer.py first.")
        return

    with open(instruction_path, "r", encoding="utf-8") as f:
        instructions = f.read()

    print(f"⚡ Compute Scientist is reading instructions from {instruction_path}...")

    # Re-using your successful 3-attempt resilient block
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"⏳ Calling Gemini API (Attempt {attempt + 1}/{max_retries})...")
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=f"Please build the compute engine components required by these instructions:\n\n{instructions}",
                config=types.GenerateContentConfig(
                    system_instruction=compute_persona,
                    temperature=0.2,
                    response_mime_type="application/json",
                )
            )
            break
            
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    print("⚠️ Servers are busy. Waiting 10 seconds before retrying...")
                    time.sleep(10)
                else:
                    print("❌ API is still busy after 3 attempts. Please try again later.")
                    return
            else:
                raise e

    try:
        generated_payload = json.loads(response.text)
        files = generated_payload.get("files", [])
        
        base_compute_dir = "../compute-python"
        print(f"\n🚀 Writing generated files to '{base_compute_dir}':")
        
        for file_info in files:
            target_path = os.path.join(base_compute_dir, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_info["code"])
            print(f"  ✅ Created: {file_info['path']}")
            
        print("\n🎉 Python Compute codebase successfully scaffolded by the agent!")

    except json.JSONDecodeError:
        print("❌ Error: Failed to parse JSON payload. Raw response:")
        print(response.text)

if __name__ == "__main__":
    run_compute_agent("prompt_for_compute_scientist_python_fastapi.txt")