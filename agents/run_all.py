import os
import sys
import json
import time
import subprocess
import requests

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BOARD_FILE = os.path.join(PROJECT_ROOT, "antigravity_board.json")

def load_board():
    """Loads the Kanban board state."""
    if not os.path.exists(BOARD_FILE):
        return {"todo": [], "in_progress": [], "in_review": [], "done": []}
    
    try:
        with open(BOARD_FILE, "r", encoding="utf-8") as f:
            board = json.load(f)
            for col in ["todo", "in_progress", "in_review", "done"]:
                if col not in board:
                    board[col] = []
            return board
    except Exception:
        return {"todo": [], "in_progress": [], "in_review": [], "done": []}

def save_board(board):
    """Saves the Kanban board state."""
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=4)

def fix_nextjs_code(code: str) -> str:
    """Automatically injects 'use client' and fixes router imports for Next.js App Router."""
    if not code.strip():
        return code
        
    code = code.replace("import { useRouter } from 'next/router';", "import { useRouter } from 'next/navigation';")
    code = code.replace('import { useRouter } from "next/router";', 'import { useRouter } from "next/navigation";')
    
    needs_client = any(hook in code for hook in ["useState", "useEffect", "useContext", "useRef", "useCallback", "useMemo"])
    has_client_directive = '"use client";' in code or "'use client';" in code
    
    if needs_client and not has_client_directive:
        code = '"use client";\n' + code
        
    return code

def process_ticket(ticket):
    """Passes the ticket to the 3070 Ti and overwrites the target file."""
    print(f"\n🚀 [Dispatcher] Picking up Ticket: [{ticket['id']}] for '{ticket['agent']}'")
    
    target_file = ticket.get('target_file', '').strip()
    
    while target_file and target_file[-1] in ['/', '\\', '.']:
        target_file = target_file[:-1]
        
    if not target_file:
        print(f"⚠️ [Dispatcher] Ticket [{ticket['id']}] has an empty or invalid target_file! Skipping.")
        return False
        
    base_dirs = {
        "frontend": os.path.join(PROJECT_ROOT, "frontend-nextjs"),
        "compute": os.path.join(PROJECT_ROOT, "compute-python"),
        "enterprise": os.path.join(PROJECT_ROOT, "backend-java"),
        "devops": PROJECT_ROOT,
        "qa": os.path.join(PROJECT_ROOT, "qa-tests")
    }
    
    base_dir = base_dirs.get(ticket['agent'], PROJECT_ROOT)
    full_path = os.path.abspath(os.path.join(base_dir, target_file))
    
    if os.path.isdir(full_path):
        print(f"⚠️ [Dispatcher] Target '{full_path}' evaluates to a directory, not a file! Skipping.")
        return False
    
    existing_content = ""
    try:
        if os.path.exists(full_path) and os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                existing_content = f.read()
    except Exception as e:
        print(f"⚠️ [Dispatcher] Could not read existing file {full_path}: {e}. Treating as empty.")

    system_prompt = f"""
    You are an expert {ticket['agent']} developer.
    Your task is to write or update code for the file: {target_file}.
    
    You must output ONLY the raw, complete file content. 
    Do NOT wrap the output in markdown backticks (like ```python or ```tsx).
    Do NOT include any explanations or conversational text.
    Output EXACTLY what should be written to the file.
    """

    if existing_content:
        system_prompt += f"\n\nHere is the EXISTING content of the file. Please apply the requested changes to it:\n\n{existing_content}"

    print(f"⚙️  Spinning up 3070 Ti to generate code for {target_file}...")
    
    try:
        OLLAMA_URL = "http://localhost:11434/api/generate"
        LOCAL_MODEL = "qwen2.5-coder:7b"
        
        payload = {
            "model": LOCAL_MODEL,
            "prompt": ticket['description'],
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 8000
            }
        }
        
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        generated_code = response.json().get("response", "").strip()
        
        if generated_code.startswith("```"):
            lines = generated_code.split("\n")
            if len(lines) > 1:
                generated_code = "\n".join(lines[1:])
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
            
        if ticket['agent'] == "frontend" and (target_file.endswith(".tsx") or target_file.endswith(".ts")):
            generated_code = fix_nextjs_code(generated_code)
            
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(generated_code.strip() + "\n")
            
        print(f"✅ [Dispatcher] Successfully wrote to {full_path}")
        return True
    except Exception as e:
        print(f"❌ [Dispatcher] Error processing ticket: {e}")
        return False

def trigger_deployment(agent_tag):
    service_map = {
        "compute": "compute-python",
        "enterprise": "backend-java"
    }
    
    service = service_map.get(agent_tag)
    
    if service:
        print(f"🐳 [Dispatcher] Hot-reloading Docker service: {service}...")
        subprocess.run(["docker", "compose", "build", service], cwd=PROJECT_ROOT)
        subprocess.run(["docker", "compose", "up", "-d", service], cwd=PROJECT_ROOT)
        print("✅ [Dispatcher] Deployment triggered.")

def main():
    print("===================================================")
    print("🛸 ANTIGRAVITY DISPATCHER ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Watching antigravity_board.json for new tickets...")
    print("===================================================")
    
    board = load_board()
    if board.get("in_progress") and len(board["in_progress"]) > 0:
        print(f"🔄 [Dispatcher] Reclaiming {len(board['in_progress'])} stuck tickets from 'in_progress' back to 'todo'...")
        board["todo"] = board["in_progress"] + board.get("todo", [])
        board["in_progress"] = []
        save_board(board)
    
    while True:
        board = load_board()
        
        if board.get("todo") and len(board["todo"]) > 0:
            ticket = board["todo"].pop(0)
            board["in_progress"].append(ticket)
            save_board(board)
            
            success = process_ticket(ticket)
            
            board = load_board() 
            board["in_progress"] = [t for t in board["in_progress"] if t["id"] != ticket["id"]]
            
            if success:
                if ticket["agent"] == "frontend":
                    print(f"📫 [Dispatcher] Routing frontend ticket [{ticket['id']}] to UX/UI Designer...")
                    board["in_review"].append(ticket)
                elif ticket["agent"] in ["compute", "enterprise"]:
                    print(f"📫 [Dispatcher] Routing backend ticket [{ticket['id']}] to QA Gatekeeper...")
                    board["in_review"].append(ticket)
                    # Deploy the new backend code so QA can execute tests against the live container!
                    trigger_deployment(ticket["agent"])
                else:
                    board["done"].append(ticket)
            else:
                retries = ticket.get("retries", 0)
                if retries < 2:
                    print(f"⚠️ Ticket failed. Putting it at the back of the queue (Retry {retries + 1}/3).")
                    ticket["retries"] = retries + 1
                    board["todo"].append(ticket)
                else:
                    print(f"🛑 Ticket [{ticket['id']}] failed 3 times! Moving to 'done' (as failed).")
                    ticket["status"] = "failed"
                    board["done"].append(ticket)
                
            save_board(board)
                
        time.sleep(3)

if __name__ == "__main__":
    main()