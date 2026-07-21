import os
import sys
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

architect_persona = """
You are an elite System Architect.
Your job is to read a product specification document and design a complete, highly optimized microservice architecture.

You must output a strictly formatted JSON object representing the system blueprint.
The JSON must contain the following top-level keys:
1. "project_name": A string representing the system name.
2. "frontend": An object detailing Next.js components, page routes, and state management.
3. "compute_engine": An object detailing the Python FastAPI data-processing endpoints and required Python libraries.
4. "enterprise_backend": An object detailing the Java Spring Boot REST API endpoints, core business logic, and Database entity models (Tables & Columns).

CRITICAL: Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks or add conversational text.
"""

def run_architect():
    print("\n📐 System Architect Booting Up...")
    
    # 1. Read the Master Specification created by the Mother Agent
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        print(f"❌ Error: '{req_file}' not found. Please run mother_agent.py first to generate the idea.")
        sys.exit(1)

    with open(req_file, "r", encoding="utf-8") as f:
        project_requirements = f.read()

    print("📄 Analyzing Master Specification...")

    user_content = f"""
    Based on the following product specification, design the system architecture blueprint.
    Ensure the responsibilities are clearly split between the Next.js Frontend (UI), the Python Compute Engine (heavy processing), and the Java Enterprise Backend (Database & Business Logic).
    
    Product Specification:
    {project_requirements}
    """

    # 2. Call Gemini with Retry Logic
    for attempt in range(3):
        try:
            print(f"⏳ Calling Gemini API to design blueprint (Attempt {attempt + 1}/3)...")
            response = client.models.generate_content(
                model='gemini-1.5-pro', # Pro model used for deep architectural reasoning
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=architect_persona,
                    temperature=0.2, # Low temperature for highly structured, predictable JSON
                    response_mime_type="application/json",
                )
            )
            print("✅ Architecture designed successfully!")
            break
        except Exception as e:
            error_str = str(e)
            print(f"⚠️ API Error caught: {type(e).__name__} - {error_str}")
            if "503" in error_str or "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print("💤 Token limit or traffic spike reached. Sleeping 20 seconds before retry...")
                time.sleep(20)
            else:
                raise e

    # 3. Clean and Parse the JSON Output
    try:
        raw_text = response.text.strip()
        
        # Strip markdown backticks if the LLM ignores instructions
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        blueprint_data = json.loads(raw_text.strip())
        
        # 4. Save the Blueprint for the next agents
        output_file = "system_blueprint.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(blueprint_data, f, indent=4)
            
        print(f"🎉 System Blueprint successfully saved to '{output_file}'!")

    except json.JSONDecodeError:
        print("❌ Error: Failed to parse JSON payload. Raw response:")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    run_architect()