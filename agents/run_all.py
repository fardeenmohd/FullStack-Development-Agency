import os
import sys
import json
import time
import subprocess
import requests

# Ensure we can import local_llm if run_all.py is inside the agents folder
sys.path.append(os.path.dirname(__file__))
try:
    from local_llm import generate_local_code
except ImportError:
    pass # We will use direct requests for raw file output below

# Set PROJECT_ROOT to the parent directory since this script is in 'agents/'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BOARD_FILE = os.path.join(PROJECT_ROOT, "antigravity_board.json")

def load_board():
    """Loads the Kanban board state."""
    if not os.path.exists(BOARD_FILE):
        return {"todo": [], "in_progress": [], "done": []}
    with open(BOARD_FILE, "r") as f:
        return json.load(f)

def save_board(board):
    """Saves the Kanban board state."""
    with open(BOARD_FILE, "w") as f:
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
    target_file = ticket['target_file']
    
    # Resolve actual path based on agent
    base_dirs = {
        "frontend": os.path.join(PROJECT_ROOT, "frontend-nextjs"),
        "compute": os.path.join(PROJECT_ROOT, "compute-python"),
        "enterprise": os.path.join(PROJECT_ROOT, "backend-java"),
        "devops": PROJECT_ROOT,
        "qa": os.path.join(PROJECT_ROOT, "qa-tests")
    }
    
    base_dir = base_dirs.get(ticket['agent'], PROJECT_ROOT)
    full_path = os.path.join(base_dir, target_file)
    
    # Read existing content if the file already exists
    existing_content = ""
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            existing_content = f.read()

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
        # We bypass local_llm.py here because we want raw text output, not strict JSON
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
        
        # Strip markdown if the AI hallucinates it
        if generated_code.startswith("```"):
            lines = generated_code.split("\n")
            if len(lines) > 1:
                generated_code = "\n".join(lines[1:])
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
            
        # Apply Next.js auto-fixes if it's a frontend file
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
    """Triggers docker rebuild for the specific container modified by the ticket."""
    service_map = {
        "frontend": "frontend-nextjs",
        "compute": "compute-python",
        "enterprise": "backend-java"
    }
    service = service_map.get(agent_tag)
    
    if service:
        print(f"🐳 [Dispatcher] Hot-reloading Docker service: {service}...")
        subprocess.run(["docker", "compose", "build", service], cwd=PROJECT_ROOT)
        subprocess.run(["docker", "compose", "up", "-d", service], cwd=PROJECT_ROOT)
    else:
        print("🐳 [Dispatcher] Rebuilding entire Docker stack...")
        subprocess.run(["docker", "compose", "up", "--build", "-d"], cwd=PROJECT_ROOT)
        
    print("✅ [Dispatcher] Deployment triggered. SRE Agent will catch any runtime errors.")

def main():
    print("===================================================")
    print("🛸 ANTIGRAVITY DISPATCHER ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Watching antigravity_board.json for new tickets...")
    print("===================================================")
    
    # Ensure board exists
    if not os.path.exists(BOARD_FILE):
        save_board({"todo": [], "in_progress": [], "done": []})
    
    while True:
        board = load_board()
        
        if board.get("todo") and len(board["todo"]) > 0:
            # Pop the first ticket
            ticket = board["todo"].pop(0)
            board["in_progress"].append(ticket)
            save_board(board)
            
            success = process_ticket(ticket)
            
            # Reload in case PO agent added more tickets while we were generating
            board = load_board() 
            
            # Remove from in_progress
            board["in_progress"] = [t for t in board["in_progress"] if t["id"] != ticket["id"]]
            
            if success:
                board["done"].append(ticket)
            else:
                # Put back in todo if failed 
                print("⚠️ Putting ticket back in TODO due to failure.")
                board["todo"].insert(0, ticket)
                
            save_board(board)
            
            if success:
                trigger_deployment(ticket["agent"])
                
        # Poll every 3 seconds
        time.sleep(3)

if __name__ == "__main__":
    main()