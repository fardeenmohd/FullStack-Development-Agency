import os
import json
import time # 👈 Add this new import
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

frontend_persona = """
You are an expert Senior Frontend Engineer specializing in React, Next.js, and TypeScript.
Your job is to read specific development instructions and generate clean, component-driven UI code.

You must follow modern React best practices:
- Use functional components with TypeScript types.
- Ensure clean layout structures and modular component patterns.
- Manage component state gracefully.

You MUST output a strictly formatted JSON object containing:
1. "files": An array of objects, where each object has:
   - "path": The target filename/filepath (e.g., "components/Dashboard.tsx")
   - "code": The full, un-truncated string content of the code file.
"""

def run_frontend_agent(instruction_path: str):
    if not os.path.exists(instruction_path):
        print(f"❌ Error: {instruction_path} not found. Run synthesizer.py first.")
        return

    with open(instruction_path, "r", encoding="utf-8") as f:
        instructions = f.read()

    print(f"🎨 Frontend Specialist is reading instructions from {instruction_path}...")

    # 👇 Added Retry Logic Here 👇
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"⏳ Calling Gemini API (Attempt {attempt + 1}/{max_retries})...")
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=f"Please build the UI modules required by these instructions:\n\n{instructions}",
                config=types.GenerateContentConfig(
                    system_instruction=frontend_persona,
                    temperature=0.2,
                    response_mime_type="application/json",
                )
            )
            break # If successful, break out of the retry loop
            
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    print("⚠️ Servers are busy. Waiting 10 seconds before retrying...")
                    time.sleep(10)
                else:
                    print("❌ API is still busy after 3 attempts. Please try again later.")
                    return
            else:
                # If it's a different error, raise it immediately
                raise e

    # Proceed with saving files...
    try:
        generated_payload = json.loads(response.text)
        files = generated_payload.get("files", [])
        
        base_frontend_dir = "../frontend-nextjs"
        print(f"\n🚀 Writing generated files to '{base_frontend_dir}':")
        
        for file_info in files:
            target_path = os.path.join(base_frontend_dir, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_info["code"])
            print(f"  ✅ Created: {file_info['path']}")
            
        print("\n🎉 Frontend codebase successfully scaffolded by the agent!")

    except json.JSONDecodeError:
        print("❌ Error: Failed to parse JSON payload. Raw response:")
        print(response.text)

if __name__ == "__main__":
    run_frontend_agent("prompt_for_frontend_specialist_next.js_typescript.txt")