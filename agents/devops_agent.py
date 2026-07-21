import os
import json
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

devops_persona = """
You are an expert DevOps Architect.
Your job is to read a system blueprint and generate the infrastructure-as-code files required to deploy the system.

You must output a strictly formatted JSON object containing:
1. "files": An array of objects, where each object has:
   - "path": The target filename (e.g., "docker-compose.yml", "frontend-nextjs/Dockerfile", "compute-python/Dockerfile", "backend-java/Dockerfile")
   - "code": The full string content of the configuration file.

Ensure the Dockerfiles follow best practices (multi-stage builds, lightweight Alpine/Slim base images) and the docker-compose.yml correctly networks the 3 services together, exposing the right ports.
"""

def run_devops_agent(blueprint_path: str):
    if not os.path.exists(blueprint_path):
        print(f"❌ Error: {blueprint_path} not found. Run architect.py first.")
        sys.exit(1)

    with open(blueprint_path, "r") as f:
        blueprint_data = json.load(f)

    print("🐳 DevOps Architect is designing the container infrastructure...")

    user_content = f"""
    Based on the following architecture blueprint, generate a root `docker-compose.yml` and the required `Dockerfile` for each of the three services (Frontend, Compute Engine, Enterprise Backend).
    
    Blueprint:
    {json.dumps(blueprint_data, indent=2)}
    """

    try:
        print("⏳ Calling Gemini API for Infrastructure Generation...")
        response = client.models.generate_content(
            model='gemini-3.5-flash', # Or your working model string
            contents=user_content,
            config=types.GenerateContentConfig(
                system_instruction=devops_persona,
                temperature=0.1,
                response_mime_type="application/json",
            )
        )
        print("✅ Connection successful!")
        
    except Exception as e:
        error_str = str(e)
        if "503" in error_str or "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            print("❌ API limit or server error reached. Exiting script to let Orchestrator handle the wait.")
            sys.exit(1)
        else:
            raise e

    try:
        generated_payload = json.loads(response.text)
        files = generated_payload.get("files", [])
        
        base_dir = "../" 
        print(f"\n🚀 Writing generated infrastructure files:")
        
        for file_info in files:
            target_path = os.path.join(base_dir, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_info["code"])
            print(f"  ✅ Created: {file_info['path']}")
            
        print("\n🎉 Infrastructure-as-code successfully scaffolded!")

    except json.JSONDecodeError:
        print("❌ Error: Failed to parse JSON payload. Raw response:")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    run_devops_agent("system_blueprint.json")