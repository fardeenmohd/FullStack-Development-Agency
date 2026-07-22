import os
import sys
import json
import time
import subprocess
import requests

# Set up robust absolute paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BOARD_FILE = os.path.join(PROJECT_ROOT, "antigravity_board.json")

OLLAMA_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL = "qwen2.5-coder:7b"
CHECK_INTERVAL = 10 # Poll every 10 seconds

def load_board():
    """Loads the Kanban board state."""
    if not os.path.exists(BOARD_FILE):
        return {"todo": [], "in_progress": [], "in_review": [], "done": [], "archived": []}
    try:
        with open(BOARD_FILE, "r", encoding="utf-8") as f:
            board = json.load(f)
            # Auto-heal missing columns
            for col in ["todo", "in_progress", "in_review", "done", "archived"]:
                if col not in board:
                    board[col] = []
            return board
    except Exception:
        return {"todo": [], "in_progress": [], "in_review": [], "done": [], "archived": []}

def save_board(board):
    """Saves the Kanban board state."""
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=4)

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

def process_ui_review(ticket):
    """Sends the frontend code to the local LLM for UX/UI polishing."""
    print(f"\n💅 [Designer] Reviewing UI for Ticket: [{ticket['id']}] -> {ticket['target_file']}")
    
    target_file = ticket.get('target_file', '').strip()
    full_path = os.path.abspath(os.path.join(PROJECT_ROOT, "frontend-nextjs", target_file))
    
    if not os.path.exists(full_path):
        print(f"⚠️ [Designer] File {full_path} not found. Skipping review.")
        return False

    with open(full_path, "r", encoding="utf-8") as f:
        existing_code = f.read()

    system_prompt = """
    You are an elite UX/UI Designer and Frontend Architect.
    Your job is to take functional Next.js/Tailwind code and elevate it to a premium, cohesive, SaaS-grade design.

    CRITICAL DESIGN SYSTEM RULES:
    1. Spacing: Enforce consistent padding/margins. Use generous whitespace.
    2. Typography: Ensure clear visual hierarchy (e.g., text-sm text-gray-400 for subtext, text-xl font-semibold for headers).
    3. Colors: Apply a cohesive, modern palette. Fix clashing colors.
    4. Polish & A11y: Add hover states (e.g., hover:bg-gray-800), smooth transitions (transition-colors duration-200), and rounded corners (rounded-lg).
    5. Responsiveness: Ensure it stacks correctly on mobile (e.g., flex-col md:flex-row).
    6. DO NOT break any React logic, hooks, data fetching, or existing functionality. ONLY upgrade the Tailwind classes and JSX structure.
    
    You MUST output ONLY the raw, complete file content. 
    Do NOT wrap the output in markdown backticks.
    Do NOT include explanations.
    """

    print(f"✨  Applying SaaS Design System to {os.path.basename(full_path)}...")
    
    try:
        payload = {
            "model": LOCAL_MODEL,
            "prompt": f"Here is the functional code. Polish the UI and return the full file:\n\n{existing_code}",
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2, # Slightly higher temp for design creativity
                "num_predict": 8000
            }
        }
        
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        polished_code = response.json().get("response", "").strip()
        
        # Strip markdown if the AI hallucinated it
        if polished_code.startswith("```"):
            lines = polished_code.split("\n")
            if len(lines) > 1:
                polished_code = "\n".join(lines[1:])
        if polished_code.endswith("```"):
            polished_code = polished_code[:-3]
            
        # Apply Next.js safety fixes
        if target_file.endswith(".tsx") or target_file.endswith(".ts"):
            polished_code = fix_nextjs_code(polished_code)
            
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(polished_code.strip() + "\n")
            
        print(f"✅ [Designer] UI Polish complete for {os.path.basename(full_path)}!")
        return True
    except Exception as e:
        print(f"❌ [Designer] Error during UI Polish: {e}")
        return False

def trigger_frontend_deployment():
    print(f"🐳 [Designer] Hot-reloading frontend container with new polished UI...")
    subprocess.run(["docker", "compose", "build", "frontend-nextjs"], cwd=PROJECT_ROOT)
    subprocess.run(["docker", "compose", "up", "-d", "frontend-nextjs"], cwd=PROJECT_ROOT)

def main():
    print("===================================================")
    print("💅 UX/UI DESIGNER AGENT ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Watching 'in_review' column for frontend tasks...")
    print("===================================================")
    
    while True:
        board = load_board()
        
        # Find the first frontend ticket in the review column
        review_tickets = board.get("in_review", [])
        frontend_ticket = next((t for t in review_tickets if t.get("agent") == "frontend"), None)
        
        if frontend_ticket:
            # Remove it from in_review queue immediately so we don't double-process
            board["in_review"] = [t for t in review_tickets if t["id"] != frontend_ticket["id"]]
            save_board(board)
            
            success = process_ui_review(frontend_ticket)
            
            # Reload board to ensure we don't overwrite changes from other agents
            board = load_board()
            
            if success:
                board["done"].append(frontend_ticket)
                trigger_frontend_deployment()
            else:
                print(f"⚠️ [Designer] Review failed. Kicking back to 'todo' for dispatcher to try rewriting.")
                board["todo"].append(frontend_ticket)
                
            save_board(board)
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()