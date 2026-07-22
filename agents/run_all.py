import os
import time
import subprocess
from agency_utils import load_board, save_board, get_project_root
from local_llm import generate_local_code

PROJECT_ROOT = get_project_root()

def fix_nextjs_code(code: str) -> str:
    """Injects 'use client' and missing React imports."""
    import re
    if not code.strip(): return code
    code = code.replace("import { useRouter } from 'next/router';", "import { useRouter } from 'next/navigation';")
    hooks = ["useState", "useEffect", "useContext", "useRef", "useCallback"]
    needs_client = any(hook in code for hook in hooks)
    if needs_client and '"use client";' not in code and "'use client';" not in code:
        code = '"use client";\n' + code
    for hook in hooks:
        if re.search(rf'\b{hook}\b', code) and not re.search(rf'import\s+.*?\b{hook}\b.*?from\s+[\'"]react[\'"]', code, re.DOTALL):
            code = f"import {{ {hook} }} from 'react';\n" + code
    return code

def process_ticket(ticket):
    """Passes the ticket to the 3070 Ti and overwrites the target file."""
    print(f"\n🚀 [Dispatcher] Picking up Ticket: [{ticket['id']}] for '{ticket['agent']}'")
    
    target_file = ticket.get('target_file', '').strip()
    if not target_file: return False
        
    base_dirs = {
        "frontend": os.path.join(PROJECT_ROOT, "frontend-nextjs"),
        "compute": os.path.join(PROJECT_ROOT, "compute-python"),
        "enterprise": os.path.join(PROJECT_ROOT, "backend-java"),
        "devops": PROJECT_ROOT,
        "qa": os.path.join(PROJECT_ROOT, "qa-tests")
    }
    
    full_path = os.path.abspath(os.path.join(base_dirs.get(ticket['agent'], PROJECT_ROOT), target_file))
    existing_content = ""
    if os.path.exists(full_path) and os.path.isfile(full_path):
        with open(full_path, "r", encoding="utf-8") as f: existing_content = f.read()

    system_prompt = f"You are an expert {ticket['agent']} developer. Output ONLY raw file content for {target_file}. No markdown blocks."
    user_prompt = ticket['description']
    if existing_content:
        user_prompt += f"\n\nEXISTING CONTENT:\n{existing_content}"

    # OPTIMIZATION: All API logic, markdown stripping, and retries are now handled by 1 line of code
    generated_code = generate_local_code(system_prompt, user_prompt, expect_json=False)
        
    if ticket['agent'] == "frontend" and target_file.endswith((".tsx", ".ts")):
        generated_code = fix_nextjs_code(generated_code)
        
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(generated_code.strip() + "\n")
        
    print(f"✅ [Dispatcher] Successfully wrote to {full_path}")
    return True

def main():
    print("===================================================")
    print("🛸 ANTIGRAVITY DISPATCHER ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("===================================================")
    
    # --- AUTO-RECOVERY SWEEP ---
    board = load_board()
    if board.get("in_progress"):
        print(f"🧹 [Dispatcher] Auto-Recovery: Found {len(board['in_progress'])} stuck tickets. Moving back to 'todo'...")
        board["todo"] = board["in_progress"] + board.get("todo", [])
        board["in_progress"] = []
        save_board(board)
    # ---------------------------
    
    while True:
        board = load_board()
        if board.get("todo") and len(board["todo"]) > 0:
            ticket = board["todo"].pop(0)
            board["in_progress"].append(ticket)
            save_board(board)
            
            try:
                success = process_ticket(ticket)
            except Exception as e:
                print(f"❌ [Dispatcher] Fatal error processing ticket: {e}")
                success = False
            
            board = load_board() 
            board["in_progress"] = [t for t in board["in_progress"] if t["id"] != ticket["id"]]
            
            if success:
                if ticket["agent"] == "frontend":
                    board["in_review"].append(ticket)
                elif ticket["agent"] in ["compute", "enterprise"]:
                    board["in_review"].append(ticket)
                    if ticket["agent"] == "compute":
                        subprocess.run(["docker", "compose", "build", "compute-python"], cwd=PROJECT_ROOT)
                        subprocess.run(["docker", "compose", "up", "-d", "compute-python"], cwd=PROJECT_ROOT)
                else:
                    board["done"].append(ticket)
            else:
                ticket["retries"] = ticket.get("retries", 0) + 1
                if ticket["retries"] < 3: board["todo"].append(ticket)
                else: 
                    ticket["status"] = "failed"
                    board["done"].append(ticket)
            save_board(board)
        time.sleep(3)

if __name__ == "__main__":
    main()