import os
import json
import sys
from local_llm import generate_local_code

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
    tests ONLY for the {target_tier} using {tool_stack}.

    CRITICAL GPU LIMITATION: You are running on a local 8GB GPU. To prevent token overflow and truncated JSON, you MUST limit your generation to ONLY the 3 most critical test files. Do not generate every possible test.
    
    Blueprint:
    {json.dumps(blueprint_data, indent=2)}
    """
    
    try:
        generated_payload = generate_local_code(qa_persona, user_content)
        files = generated_payload.get("files", [])
        
        target_path_base = os.path.join("../qa-tests", output_dir)
        print(f"🚀 Writing generated {target_tier} tests to '{target_path_base}':")
        
        for file_info in files:
            target_path = os.path.join(target_path_base, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_info["code"])
            print(f"  ✅ Created: {file_info['path']}")
            
    except Exception as e:
        print(f"❌ Error generating tests for {target_tier}: {e}")
        sys.exit(1)


def run_qa_agent(blueprint_path: str):
    if not os.path.exists(blueprint_path):
        print(f"❌ Error: {blueprint_path} not found.")
        sys.exit(1)

    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint_data = json.load(f)

    # Generate tests locally using the 3070 Ti! No need to sleep for limits anymore!
    run_qa_chunk(blueprint_data, "Next.js Frontend", "Jest and React Testing Library", "frontend")
    run_qa_chunk(blueprint_data, "Python FastAPI Compute Engine", "PyTest", "compute")
    run_qa_chunk(blueprint_data, "Java Spring Boot Backend", "JUnit 5 and Mockito", "enterprise")
    
    print("\n🎉 ALL QA Automation scripts successfully scaffolded via Local GPU!")

if __name__ == "__main__":
    run_qa_agent("system_blueprint.json")