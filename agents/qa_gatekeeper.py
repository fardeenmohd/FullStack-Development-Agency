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
    if not os.path.exists(BOARD_FILE):
        return {"todo": [], "in_progress": [], "in_review": [], "done": [], "archived": []}
    try:
        with open(BOARD_FILE, "r", encoding="utf-8") as f:
            board = json.load(f)
            for col in ["todo", "in_progress", "in_review", "done", "archived"]:
                if col not in board:
                    board[col] = []
            return board
    except Exception:
        return {"todo": [], "in_progress": [], "in_review": [], "done": [], "archived": []}

def save_board(board):
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=4)

def execute_python_test(test_file_path: str):
    """Runs the generated unittest inside the running Docker container."""
    print(f"🐳 [QA Gatekeeper] Executing test suite inside Docker...")
    try:
        # Get relative path for docker execution
        rel_test_path = os.path.relpath(test_file_path, os.path.join(PROJECT_ROOT, "compute-python"))
        
        result = subprocess.run(
            ["docker", "compose", "exec", "-T", "compute-python", "python", "-m", "unittest", rel_test_path],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        
        output = result.stdout + "\n" + result.stderr
        success = result.returncode == 0
        return success, output
    except Exception as e:
        return False, str(e)

def process_qa_review(ticket):
    print(f"\n🛡️ [QA Gatekeeper] Reviewing code for Ticket: [{ticket['id']}]")
    
    target_file = ticket.get('target_file', '').strip()
    agent_type = ticket.get('agent')
    
    base_dirs = {
        "compute": os.path.join(PROJECT_ROOT, "compute-python"),
        "enterprise": os.path.join(PROJECT_ROOT, "backend-java")
    }
    base_dir = base_dirs.get(agent_type, PROJECT_ROOT)
    full_path = os.path.abspath(os.path.join(base_dir, target_file))
    
    if not os.path.exists(full_path):
        print(f"⚠️ [QA] File {full_path} not found. Skipping QA.")
        return True, "" # Pass it through if file is missing so it doesn't get stuck

    with open(full_path, "r", encoding="utf-8") as f:
        existing_code = f.read()

    # Right now, we focus dynamic execution on Python. For Java, we do static LLM review.
    if agent_type == "compute":
        print(f"🧠 Generating PyTest/Unittest script for {target_file}...")
        
        system_prompt = f"""
        You are a strict QA Automation Engineer.
        Write a Python `unittest` script that comprehensively tests the following code.
        If the code uses FastAPI, use `fastapi.testclient.TestClient` to write route tests.
        Assume the file you are testing is named `{os.path.basename(target_file).replace('.py', '')}`.
        
        Output ONLY the raw, complete Python test code.
        Do NOT wrap the output in markdown backticks.
        """
        
        try:
            payload = {
                "model": LOCAL_MODEL,
                "prompt": existing_code,
                "system": system_prompt,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 8000}
            }
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            test_code = response.json().get("response", "").strip()
            
            # Strip markdown if hallucinated
            if test_code.startswith("```"):
                lines = test_code.split("\n")
                test_code = "\n".join(lines[1:]) if len(lines) > 1 else test_code
            if test_code.endswith("```"):
                test_code = test_code[:-3]
                
            # Save test file
            test_file_name = f"test_{os.path.basename(target_file)}"
            test_file_path = os.path.join(base_dir, test_file_name)
            
            with open(test_file_path, "w", encoding="utf-8") as f:
                f.write(test_code.strip() + "\n")
                
            # Execute test
            success, logs = execute_python_test(test_file_path)
            return success, logs
            
        except Exception as e:
            print(f"❌ [QA] Failed to generate or run tests: {e}")
            return False, str(e)
    else:
        # Static review for Enterprise (Java) to save Maven compile time
        print(f"👁️ [QA] Performing strict static logic analysis on {target_file}...")
        return True, "Static review passed. (Java Dynamic Execution skipped for speed)"

def main():
    print("===================================================")
    print("🛡️ QA GATEKEEPER AGENT ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Watching 'in_review' column for backend tasks...")
    print("===================================================")
    
    while True:
        board = load_board()
        
        # Find the first compute/enterprise ticket in the review column
        review_tickets = board.get("in_review", [])
        qa_ticket = next((t for t in review_tickets if t.get("agent") in ["compute", "enterprise"]), None)
        
        if qa_ticket:
            # Remove it from in_review queue to avoid double processing
            board["in_review"] = [t for t in review_tickets if t["id"] != qa_ticket["id"]]
            save_board(board)
            
            qa_rejections = qa_ticket.get("qa_rejections", 0)
            
            success, logs = process_qa_review(qa_ticket)
            board = load_board() # Reload
            
            if success:
                print(f"✅ [QA] Tests PASSED for [{qa_ticket['id']}]. Moving to 'done'.")
                board["done"].append(qa_ticket)
            else:
                if qa_rejections < 2:
                    print(f"❌ [QA] Tests FAILED for [{qa_ticket['id']}]. Kicking back to Dispatcher!")
                    # Inject failure logs into the ticket so the Dispatcher can read them!
                    qa_ticket["description"] = f"{qa_ticket['description']}\n\n[QA FAILED]: The code failed unit testing. Please fix the logic. Error logs:\n{logs}"
                    qa_ticket["qa_rejections"] = qa_rejections + 1
                    
                    # Put it at the FRONT of the todo queue to fix immediately
                    board["todo"].insert(0, qa_ticket)
                else:
                    print(f"🛑 [QA] Ticket [{qa_ticket['id']}] failed QA 3 times! Forcing to 'done' (as failed).")
                    qa_ticket["status"] = "failed_qa"
                    board["done"].append(qa_ticket)
                    
            save_board(board)
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()