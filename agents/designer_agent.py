import os
import sys
import time
import subprocess
from agency_utils import load_board, save_board, get_project_root
from local_llm import generate_local_code

PROJECT_ROOT = get_project_root()
CHECK_INTERVAL = 10 

def fix_nextjs_code(code: str) -> str:
    """Automatically injects 'use client', fixes router imports, and ensures React hooks are imported."""
    import re
    if not code.strip(): return code
        
    code = code.replace("import { useRouter } from 'next/router';", "import { useRouter } from 'next/navigation';")
    code = code.replace('import { useRouter } from "next/router";', 'import { useRouter } from "next/navigation";')
    
    hooks = ["useState", "useEffect", "useContext", "useRef", "useCallback", "useMemo", "Suspense"]
    needs_client = any(hook in code for hook in hooks)
    has_client_directive = '"use client";' in code or "'use client';" in code
    
    if needs_client and not has_client_directive: code = '"use client";\n' + code
        
    for hook in hooks:
        if re.search(rf'\b{hook}\b', code):
            if not re.search(rf'import\s+.*?\b{hook}\b.*?from\s+[\'"]react[\'"]', code, re.DOTALL):
                react_import_match = re.search(r'import\s+(.*?)\s+from\s+[\'"]react[\'"]', code, re.DOTALL)
                if react_import_match:
                    existing_imports = react_import_match.group(1)
                    new_imports = existing_imports.replace('{', f'{{ {hook}, ', 1) if '{' in existing_imports else f"{existing_imports}, {{ {hook} }}"
                    code = code.replace(react_import_match.group(0), f"import {new_imports} from 'react'")
                else:
                    import_stmt = f"import {{ {hook} }} from 'react';\n"
                    if '"use client";' in code: code = code.replace('"use client";', f'"use client";\n{import_stmt}', 1)
                    elif "'use client';" in code: code = code.replace("'use client';", f"'use client';\n{import_stmt}", 1)
                    else: code = import_stmt + code
    return code

def process_ui_review(ticket):
    print(f"\n💅 [Designer] Reviewing UI for Ticket: [{ticket['id']}] -> {ticket['target_file']}")
    target_file = ticket.get('target_file', '').strip()
    full_path = os.path.abspath(os.path.join(PROJECT_ROOT, "frontend-nextjs", target_file))
    
    if not os.path.exists(full_path): return False
    with open(full_path, "r", encoding="utf-8") as f: existing_code = f.read()

    system_prompt = """
    You are an elite UX/UI Designer and Frontend Architect.
    Take functional Next.js/Tailwind code and elevate it to a premium, cohesive, SaaS-grade design.
    1. Spacing: Enforce consistent padding/margins.
    2. Typography: Ensure clear visual hierarchy.
    3. Polish: Add hover states, transitions, and rounded corners.
    4. DO NOT break any React logic. ONLY upgrade Tailwind/JSX.
    Output raw code only. No markdown blocks.
    """

    # OPTIMIZATION: One line replaces 20 lines of requests and regex parsing!
    polished_code = generate_local_code(system_prompt, existing_code, expect_json=False)
            
    if target_file.endswith(".tsx") or target_file.endswith(".ts"):
        polished_code = fix_nextjs_code(polished_code)
            
    with open(full_path, "w", encoding="utf-8") as f: f.write(polished_code.strip() + "\n")
    return True

def trigger_frontend_deployment():
    print(f"🐳 [Designer] Hot-reloading frontend container with new polished UI...")
    subprocess.run(["docker", "compose", "build", "frontend-nextjs"], cwd=PROJECT_ROOT)
    subprocess.run(["docker", "compose", "up", "-d", "frontend-nextjs"], cwd=PROJECT_ROOT)

def main():
    print("===================================================")
    print("💅 UX/UI DESIGNER AGENT ONLINE")
    print("===================================================")
    
    while True:
        board = load_board()
        review_tickets = board.get("in_review", [])
        frontend_ticket = next((t for t in review_tickets if t.get("agent") == "frontend"), None)
        
        if frontend_ticket:
            board["in_review"] = [t for t in review_tickets if t["id"] != frontend_ticket["id"]]
            save_board(board)
            
            success = process_ui_review(frontend_ticket)
            board = load_board()
            
            if success:
                print(f"✅ [Designer] Polish complete for {os.path.basename(frontend_ticket['target_file'])}")
                board["done"].append(frontend_ticket)
                trigger_frontend_deployment()
            else:
                board["todo"].append(frontend_ticket)
            save_board(board)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()