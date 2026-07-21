import os
import json
import sys
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def run_qa_chunk(blueprint_data: dict, target_tier: str, tool_stack: str, output_dir: str):
    print(f"\n🛡️ QA Gatekeeper: Generating {target_tier} tests using {tool_stack}...")
    
    qa_persona = f"""
    You are a strict Quality Assurance Automation Engineer.
    Your job is to read the system blueprint and generate testing suites specifically for the {target_tier}.
    
    You must output a strictly formatted JSON object containing:
    1. "files": An array of objects, where each object has:
       - "path": The target filename (e.g., "{target_tier}_test_suite.ext")
       - "code": The full string content of the {tool_stack} testing script.
    
    CRITICAL: Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
    """
    
    user_content = f"""
    Based on the following architecture blueprint, generate a comprehensive suite of automated 
    tests ONLY for the {target_tier} using {tool_stack}. Do not generate tests for other tiers.
    
    Blueprint:
    {json.dumps(blueprint_data, indent=2)}
    """
    
    for attempt in range(3):
        try:
            print(f"⏳ Calling Gemini API (Attempt {attempt + 1}/3)...")
            response = client.models.generate_content(
                model='gemini-3.5-flash', # 👈 Make sure this matches your working model
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=qa_persona,
                    temperature=0.1,
                    response_mime_type="application/json",
                )
            )
            print("✅ Connection successful!")
            break
        except Exception as e:
            if "503" in str(e) or "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print("⚠️ Token limit or traffic spike reached. Sleeping 20 seconds before retry...")
                time.sleep(20)
            else:
                raise e

    try:
        # 👇 THE FIX: Strip markdown backticks before parsing JSON 👇
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        generated_payload = json.loads(raw_text.strip())
        files = generated_payload.get("files", [])
        
        target_path_base = os.path.join("../qa-tests", output_dir)
        print(f"🚀 Writing generated {target_tier} tests to '{target_path_base}':")
        
        for file_info in files:
            target_path = os.path.join(target_path_base, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_info["code"])
            print(f"  ✅ Created: {file_info['path']}")
            
    except json.JSONDecodeError:
        print(f"❌ Error: Failed to parse JSON for {target_tier}. Raw response:")
        print(response.text)
        sys.exit(1)


def run_qa_agent(blueprint_path: str):
    if not os.path.exists(blueprint_path):
        print(f"❌ Error: {blueprint_path} not found.")
        sys.exit(1)

    # 1. Frontend Tests
    run_qa_chunk(blueprint_data, "Next.js Frontend", "Jest and React Testing Library", "frontend")
    print("💤 Sleeping for 30 seconds to respect Token-Per-Minute limits...")
    time.sleep(30)
    
    # 2. Compute Tests
    run_qa_chunk(blueprint_data, "Python FastAPI Compute Engine", "PyTest", "compute")
    print("💤 Sleeping for 30 seconds to respect Token-Per-Minute limits...")
    time.sleep(30)
    
    # 3. Enterprise Tests
    run_qa_chunk(blueprint_data, "Java Spring Boot Backend", "JUnit 5 and Mockito", "enterprise")
    
    print("\n🎉 ALL QA Automation scripts successfully scaffolded!")

if __name__ == "__main__":
    with open("system_blueprint.json", "r") as f:
        blueprint_data = json.load(f)
    run_qa_agent("system_blueprint.json")