import os
import json
import sys
from local_llm import generate_local_code

devops_persona = """
You are an expert DevOps Architect.
Your job is to read a system blueprint and generate the infrastructure-as-code files required to deploy the system.

You must output a strictly formatted JSON object containing:
1. "files": An array of objects, where each object has:
   - "path": The target filename (e.g., "docker-compose.yml", "frontend-nextjs/Dockerfile", "compute-python/Dockerfile", "backend-java/Dockerfile")
   - "code": The full string content of the configuration file.

CRITICAL: Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
"""

def run_devops_agent(blueprint_path: str):
    if not os.path.exists(blueprint_path):
        print(f"❌ Error: {blueprint_path} not found.")
        sys.exit(1)

    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint_data = json.load(f)

    print("🐳 DevOps Architect is designing the container infrastructure...")

    user_content = f"""
    Based on the following architecture blueprint, generate a root `docker-compose.yml` and the required `Dockerfile` for each of the three services (Frontend, Compute Engine, Enterprise Backend).
    
    Blueprint:
    {json.dumps(blueprint_data, indent=2)}
    """

    try:
        generated_payload = generate_local_code(devops_persona, user_content)
        files = generated_payload.get("files", [])
        
        base_dir = "../" 
        print(f"\n🚀 Writing generated infrastructure files:")
        
        for file_info in files:
            target_path = os.path.join(base_dir, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_info["code"])
            print(f"  ✅ Created: {file_info['path']}")
            
        print("\n🎉 Infrastructure-as-code successfully scaffolded via Local GPU!")

    except Exception as e:
        print(f"❌ Error during local devops generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_devops_agent("system_blueprint.json")