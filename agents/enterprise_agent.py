import os
import json
import sys  # 👈 Added sys for clean exiting
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

enterprise_persona = """
You are an expert Enterprise Software Engineer specializing in Java and Spring Boot.
Your job is to read specific development instructions and generate a robust, transactional backend.

You must follow strict enterprise Java best practices:
- Separate concerns into Controllers, Services, and Repositories (Data Access Layer).
- Use proper Spring annotations (@RestController, @Service, @Autowired, @Transactional).
- Include standard error handling and secure authentication patterns if requested.

You MUST output a strictly formatted JSON object containing:
1. "files": An array of objects, where each object has:
   - "path": The target filename/filepath (e.g., "src/main/java/com/sinomagan/controller/AuthController.java")
   - "code": The full, un-truncated string content of the Java source file.
"""

def run_enterprise_agent(instruction_path: str):
    if not os.path.exists(instruction_path):
        print(f"❌ Error: {instruction_path} not found. Run synthesizer.py first.")
        sys.exit(1)

    with open(instruction_path, "r", encoding="utf-8") as f:
        instructions = f.read()

    print(f"☕ Enterprise Engineer is reading instructions from {instruction_path}...")

    # 👇 Cleaned up: No more infinite loop here. Orchestrator handles retries! 👇
    try:
        print("⏳ Calling Gemini API...")
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=f"Please build the Spring Boot application components required by these instructions:\n\n{instructions}",
            config=types.GenerateContentConfig(
                system_instruction=enterprise_persona,
                temperature=0.2,
                response_mime_type="application/json",
            )
        )
        print("✅ Connection successful!")
        
    except Exception as e:
        error_str = str(e)
        # If it's a quota/traffic issue, exit with an error code so run_all.py knows to sleep
        if "503" in error_str or "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            print("❌ API limit reached. Exiting script to let Orchestrator handle the 5-minute wait.")
            sys.exit(1)  # 👈 Sends failure signal to Orchestrator
        else:
            # If it's a real bug, crash loudly
            raise e

    # Proceed with saving files...
    try:
        generated_payload = json.loads(response.text)
        files = generated_payload.get("files", [])
        
        base_backend_dir = "../backend-java"
        print(f"\n🚀 Writing generated files to '{base_backend_dir}':")
        
        for file_info in files:
            target_path = os.path.join(base_backend_dir, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_info["code"])
            print(f"  ✅ Created: {file_info['path']}")
            
        print("\n🎉 Java Spring Boot backend successfully scaffolded by the agent!")

    except json.JSONDecodeError:
        print("❌ Error: Failed to parse JSON payload. Raw response:")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    run_enterprise_agent("prompt_for_enterprise_engineer_java_spring_boot.txt")