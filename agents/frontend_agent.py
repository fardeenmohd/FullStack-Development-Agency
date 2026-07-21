import os
import json
import sys
from local_llm import generate_local_code

frontend_persona = """
You are an expert Frontend Developer specializing in React, Next.js (App Router), and Tailwind CSS.
Your job is to read a system architecture blueprint and generate the frontend codebase.

You must output a strictly formatted JSON object containing:
1. "files": An array of objects, where each object has:
   - "path": The target filename (e.g., "app/page.tsx", "components/Dashboard.tsx", "package.json")
   - "code": The full string content of the file.

Ensure you include a basic package.json with the required dependencies and write modern, clean functional components.
CRITICAL: Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
"""

def run_frontend_agent(blueprint_path: str):
    if not os.path.exists(blueprint_path):
        print(f"❌ Error: {blueprint_path} not found. Run architect.py first.")
        sys.exit(1)

    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint_data = json.load(f)

    print("🎨 Frontend Agent is designing the Next.js UI...")

    user_content = f"""
    Based on the following architecture blueprint, generate the Next.js frontend repository.
    Focus on creating the core pages, components, and API integration hooks.
    
    Blueprint:
    {json.dumps(blueprint_data, indent=2)}
    """

    try:
        # The generate_local_code function handles the request, timeout, and JSON parsing!
        generated_payload = generate_local_code(frontend_persona, user_content)
        files = generated_payload.get("files", [])
        
        base_frontend_dir = "../frontend-nextjs"
        print(f"\n🚀 Writing generated frontend code to '{base_frontend_dir}':")
        
        for file_info in files:
            target_path = os.path.join(base_frontend_dir, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_info["code"])
            print(f"  ✅ Created: {file_info['path']}")
            
        print("\n🎉 Frontend codebase successfully scaffolded via Local GPU!")

    except Exception as e:
        print(f"❌ Error during local frontend generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_frontend_agent("system_blueprint.json")