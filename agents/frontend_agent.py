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

CRITICAL NEXT.JS APP ROUTER RULES:
1. Every component or page that uses React hooks (`useState`, `useEffect`, `useContext`, `useRef`) MUST start with the exact line: `"use client";` at the very top.
2. Use `import { useRouter } from 'next/navigation';` instead of 'next/router' (Next.js 13+ App Router standard).
3. Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
"""

def fix_nextjs_code(code: str) -> str:
    """Automatically injects 'use client' and fixes router imports for Next.js App Router."""
    if not code.strip():
        return code
        
    # Replace legacy router
    code = code.replace("import { useRouter } from 'next/router';", "import { useRouter } from 'next/navigation';")
    code = code.replace('import { useRouter } from "next/router";', 'import { useRouter } from "next/navigation";')
    
    # Check if client hooks are used and 'use client' is missing
    needs_client = any(hook in code for hook in ["useState", "useEffect", "useContext", "useRef", "useCallback", "useMemo"])
    has_client_directive = '"use client";' in code or "'use client';" in code
    
    if needs_client and not has_client_directive:
        code = '"use client";\n' + code
        
    return code

def run_frontend_agent(blueprint_path: str):
    if not os.path.exists(blueprint_path):
        print(f"❌ Error: {blueprint_path} not found. Run architect.py first.")
        sys.exit(1)

    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint_data = json.load(f)

    print("🎨 Frontend Agent is designing the Next.js UI...")

    user_content = f"""
    Based on the following architecture blueprint, generate the Next.js frontend repository.
    Focus on creating core pages, components, and API integration hooks using Next.js App Router standards.
    
    Blueprint:
    {json.dumps(blueprint_data, indent=2)}
    """

    try:
        generated_payload = generate_local_code(frontend_persona, user_content)
        files = generated_payload.get("files", [])
        
        base_frontend_dir = "../frontend-nextjs"
        print(f"\n🧹 Cleaning old frontend source files in '{base_frontend_dir}'...")
        if os.path.exists(os.path.join(base_frontend_dir, "app")):
            import shutil
            shutil.rmtree(os.path.join(base_frontend_dir, "app"))
        if os.path.exists(os.path.join(base_frontend_dir, "components")):
            import shutil
            shutil.rmtree(os.path.join(base_frontend_dir, "components"))
            
        print(f"\n🚀 Writing generated frontend code to '{base_frontend_dir}':")
        
        for file_info in files:
            target_path = os.path.join(base_frontend_dir, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            file_code = file_info["code"]
            if file_info["path"].endswith(".tsx") or file_info["path"].endswith(".ts"):
                file_code = fix_nextjs_code(file_code)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_code)
            print(f"  ✅ Created: {file_info['path']}")
            
        print("\n🎉 Frontend codebase successfully scaffolded via Local GPU!")

    except Exception as e:
        print(f"❌ Error during local frontend generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_frontend_agent("system_blueprint.json")