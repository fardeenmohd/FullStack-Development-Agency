import os
import json
import sys
from local_llm import generate_local_code

enterprise_persona = """
You are an expert Java Developer specializing in Spring Boot and enterprise architectures.
Your job is to read a system architecture blueprint and generate the enterprise backend codebase.

You must output a strictly formatted JSON object containing:
1. "files": An array of objects, where each object has:
   - "path": The target filename (e.g., "pom.xml", "src/main/java/com/app/Application.java")
   - "code": The full string content of the file.

CRITICAL: Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
"""

def run_enterprise_agent(blueprint_path: str):
    if not os.path.exists(blueprint_path):
        print(f"❌ Error: {blueprint_path} not found.")
        sys.exit(1)

    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint_data = json.load(f)

    print("☕ Enterprise Engineer is designing the Java Spring Boot system...")

    user_content = f"""
    Based on the following architecture blueprint, generate the Java Spring Boot repository.
    Focus on creating the REST Controllers, JPA Entities, Repositories, and pom.xml.
    
    Blueprint:
    {json.dumps(blueprint_data, indent=2)}
    """

    try:
        generated_payload = generate_local_code(enterprise_persona, user_content)
        files = generated_payload.get("files", [])
        
        base_dir = "../backend-java"
        print(f"\n🚀 Writing generated enterprise code to '{base_dir}':")
        
        for file_info in files:
            target_path = os.path.join(base_dir, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_info["code"])
            print(f"  ✅ Created: {file_info['path']}")
            
        print("\n🎉 Enterprise Backend successfully scaffolded via Local GPU!")

    except Exception as e:
        print(f"❌ Error during local enterprise generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_enterprise_agent("system_blueprint.json")