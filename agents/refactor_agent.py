import os
import json
import time
import subprocess
import requests

# Set up robust absolute paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BOARD_FILE = os.path.join(PROJECT_ROOT, "antigravity_board.json")

# Ollama settings for the local 3070 Ti
OLLAMA_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL = "qwen2.5-coder:7b"
CHECK_INTERVAL = 15 # Poll every 15 seconds

def load_board():
    """Loads the Kanban board state."""
    if not os.path.exists(BOARD_FILE):
        return {"todo": [], "in_progress": [], "done": [], "archived": []}
    try:
        with open(BOARD_FILE, "r", encoding="utf-8") as f:
            board = json.load(f)
            # Ensure the 'archived' column exists for our refactor process
            if "archived" not in board:
                board["archived"] = []
            return board
    except Exception:
        return {"todo": [], "in_progress": [], "done": [], "archived": []}

def save_board(board):
    """Saves the Kanban board state."""
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=4)

def fix_nextjs_code(code: str) -> str:
    """Ensures Next.js files don't lose their 'use client' directives during refactoring."""
    if not code.strip():
        return code
    
    needs_client = any(hook in code for hook in ["useState", "useEffect", "useContext", "useRef", "useCallback"])
    has_client_directive = '"use client";' in code or "'use client';" in code
    
    if needs_client and not has_client_directive:
        code = '"use client";\n' + code
        
    return code

def refactor_file(filepath: str, agent_type: str):
    """Sends the file to the local LLM to be cleaned up and optimized."""
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        print(f"⚠️ [Refactor] Cannot find {filepath}. Skipping.")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            original_code = f.read()
    except Exception as e:
        print(f"⚠️ [Refactor] Cannot read {filepath}: {e}")
        return False

    print(f"🧹 [Refactor] Optimizing {os.path.basename(filepath)} on the 3070 Ti...")

    system_prompt = f"""
    You are an expert Senior {agent_type.capitalize()} Software Engineer.
    Your task is to REFACTOR the provided code to improve its quality, readability, and adherence to DRY principles.
    
    CRITICAL RULES:
    1. Do NOT remove or break any existing functionality.
    2. Add helpful comments explaining complex logic.
    3. Remove unused imports or dead code.
    4. You MUST output ONLY the raw, complete file content. 
    5. Do NOT wrap the output in markdown backticks (like ```python or ```tsx).
    6. Do NOT include any explanations or conversational text.
    """

    payload = {
        "model": LOCAL_MODEL,
        "prompt": original_code,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 8000
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        refactored_code = response.json().get("response", "").strip()
        
        # Strip markdown if the AI hallucinates it
        if refactored_code.startswith("```"):
            lines = refactored_code.split("\n")
            if len(lines) > 1:
                refactored_code = "\n".join(lines[1:])
        if refactored_code.endswith("```"):
            refactored_code = refactored_code[:-3]
            
        # Apply Next.js auto-fixes if it's a frontend file
        if agent_type == "frontend" and (filepath.endswith(".tsx") or filepath.endswith(".ts")):
            refactored_code = fix_nextjs_code(refactored_code)

        # Safety check: If the LLM returned nothing or something incredibly short, reject it
        if len(refactored_code) < 10 or refactored_code == original_code:
            print(f"⚠️ [Refactor] Code unchanged or LLM returned empty for {os.path.basename(filepath)}.")
            return False

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(refactored_code.strip() + "\n")
            
        print(f"✨ [Refactor] Successfully refactored {os.path.basename(filepath)}!")
        return True
    except Exception as e:
        print(f"❌ [Refactor] Error during LLM generation: {e}")
        return False

def trigger_rebuild(services_to_rebuild: set):
    """Triggers Docker rebuild for the refactored services."""
    service_map = {
        "frontend": "frontend-nextjs",
        "compute": "compute-python",
        "enterprise": "backend-java"
    }
    
    for agent_tag in services_to_rebuild:
        service = service_map.get(agent_tag)
        if service:
            print(f"🐳 [Refactor] Re-deploying {service} to verify refactor...")
            subprocess.run(["docker", "compose", "build", service], cwd=PROJECT_ROOT)
            subprocess.run(["docker", "compose", "up", "-d", service], cwd=PROJECT_ROOT)

def run_refactor_loop():
    print("===================================================")
    print("🧹 REFACTOR AGENT ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Watching for End of Sprint (Todo=0, In Progress=0).")
    print("===================================================")
    
    base_dirs = {
        "frontend": os.path.join(PROJECT_ROOT, "frontend-nextjs"),
        "compute": os.path.join(PROJECT_ROOT, "compute-python"),
        "enterprise": os.path.join(PROJECT_ROOT, "backend-java"),
        "qa": os.path.join(PROJECT_ROOT, "qa-tests")
    }

    while True:
        board = load_board()
        
        # Check if the phase/sprint is complete
        is_sprint_done = len(board.get("todo", [])) == 0 and len(board.get("in_progress", [])) == 0
        has_completed_tickets = len(board.get("done", [])) > 0
        
        if is_sprint_done and has_completed_tickets:
            print("\n🏁 [Refactor] Phase Complete! Initiating Codebase Cleanup...")
            
            # Deduplicate target files to avoid refactoring the same file multiple times
            files_to_refactor = {}
            services_modified = set()
            
            for ticket in board["done"]:
                # Ignore failed tickets
                if ticket.get("status") == "failed":
                    continue
                    
                target = ticket.get("target_file", "").strip()
                agent = ticket.get("agent", "compute")
                
                if target:
                    base_dir = base_dirs.get(agent, PROJECT_ROOT)
                    full_path = os.path.abspath(os.path.join(base_dir, target))
                    files_to_refactor[full_path] = agent
                    services_modified.add(agent)
            
            # Refactor each file
            for filepath, agent in files_to_refactor.items():
                refactor_file(filepath, agent)
                
            # Move all done tickets to archived
            print(f"📦 [Refactor] Archiving {len(board['done'])} completed tickets...")
            board["archived"].extend(board["done"])
            board["done"] = []
            save_board(board)
            
            # Rebuild the modified docker containers to ensure the refactored code compiles!
            if services_modified:
                trigger_rebuild(services_modified)
                
            print("✅ [Refactor] Sprint Cleanup Complete. Waiting for next phase.")
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_refactor_loop()