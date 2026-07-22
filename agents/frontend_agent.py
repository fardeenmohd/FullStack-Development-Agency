import os
import json
import sys
from local_llm import generate_local_code

frontend_persona = """
You are an expert Frontend Developer specializing in React, Next.js (App Router), and Tailwind CSS.
Your job is to read a system architecture blueprint and generate the frontend codebase.

You must output a strictly formatted JSON object containing:
1. "files": An array of objects, where each object has:
   - "path": The target filename (e.g., "app/page.tsx")
   - "code": The full string content of the file.

CRITICAL NEXT.JS APP ROUTER RULES:
1. CONSOLIDATION: You MUST put all React components, hooks, and UI logic into a single `app/page.tsx` file. Do NOT generate separate `hooks/`, `components/`, or `app/login/page.tsx` files. Use inline conditional rendering.
2. DO NOT generate `app/layout.tsx` or `app/globals.css`. The system will auto-generate them.
3. Every component or page that uses React hooks (`useState`, `useEffect`) MUST start with `"use client";` at the very top.
4. Use `import { useRouter } from 'next/navigation';` instead of 'next/router'.
5. Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
"""

def fix_nextjs_code(code: str) -> str:
    """Automatically injects 'use client', fixes router imports, and ensures React hooks are imported."""
    import re
    if not code.strip():
        return code
        
    code = code.replace("import { useRouter } from 'next/router';", "import { useRouter } from 'next/navigation';")
    code = code.replace('import { useRouter } from "next/router";', 'import { useRouter } from "next/navigation";')
    
    hooks = ["useState", "useEffect", "useContext", "useRef", "useCallback", "useMemo", "Suspense"]
    needs_client = any(hook in code for hook in hooks)
    has_client_directive = '"use client";' in code or "'use client';" in code
    
    if needs_client and not has_client_directive:
        code = '"use client";\n' + code
        
    # Aggressively auto-inject missing React hook imports
    for hook in hooks:
        if re.search(rf'\b{hook}\b', code):
            if not re.search(rf'import\s+.*?\b{hook}\b.*?from\s+[\'"]react[\'"]', code, re.DOTALL):
                react_import_match = re.search(r'import\s+(.*?)\s+from\s+[\'"]react[\'"]', code, re.DOTALL)
                if react_import_match:
                    existing_imports = react_import_match.group(1)
                    if '{' in existing_imports:
                        new_imports = existing_imports.replace('{', f'{{ {hook}, ', 1)
                    else:
                        new_imports = f"{existing_imports}, {{ {hook} }}"
                    code = code.replace(react_import_match.group(0), f"import {new_imports} from 'react'")
                else:
                    import_stmt = f"import {{ {hook} }} from 'react';\n"
                    if '"use client";' in code:
                        code = code.replace('"use client";', f'"use client";\n{import_stmt}', 1)
                    elif "'use client';" in code:
                        code = code.replace("'use client';", f"'use client';\n{import_stmt}", 1)
                    else:
                        code = import_stmt + code
                        
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
            
        # Clean up any hallucinated directories from previous runs
        for bad_dir in ["hooks", "context", "pages", "lib", "app/login", "app/register", "app/dashboard"]:
            bad_path = os.path.join(base_frontend_dir, bad_dir)
            if os.path.exists(bad_path):
                import shutil
                shutil.rmtree(bad_path)
            
        print(f"\n🚀 Writing generated frontend code to '{base_frontend_dir}':")
        
        for file_info in files:
            target_path = os.path.join(base_frontend_dir, file_info["path"])
            
            # Skip model-generated layouts or styles; we auto-inject perfect ones
            if "layout.tsx" in target_path or "globals.css" in target_path:
                continue

            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            file_code = file_info["code"]
            if file_info["path"].endswith(".tsx") or file_info["path"].endswith(".ts"):
                file_code = fix_nextjs_code(file_code)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_code)
            print(f"  ✅ Created: {file_info['path']}")
            
        # AUTO-INJECT LAYOUT AND GLOBALS
        print("  ✅ Auto-injecting bulletproof app/layout.tsx and app/globals.css...")
        app_dir = os.path.join(base_frontend_dir, "app")
        os.makedirs(app_dir, exist_ok=True)
        
        with open(os.path.join(app_dir, "globals.css"), "w", encoding="utf-8") as f:
            f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")
            
        with open(os.path.join(app_dir, "layout.tsx"), "w", encoding="utf-8") as f:
            f.write("import \"./globals.css\";\n")
            f.write("export const metadata = { title: \"Lead Hunter\", description: \"B2B Platform\" };\n")
            f.write("export default function RootLayout({ children }: { children: React.ReactNode }) {\n")
            f.write("  return (\n")
            f.write("    <html lang=\"en\">\n")
            f.write("      <body>{children}</body>\n")
            f.write("    </html>\n")
            f.write("  );\n")
            f.write("}\n")

        print("\n🎉 Frontend codebase successfully scaffolded via Local GPU!")

    except Exception as e:
        print(f"❌ Error during local frontend generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_frontend_agent("system_blueprint.json")