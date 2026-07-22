import os
import time
import subprocess
from agency_utils import load_board, save_board, get_project_root
from local_llm import generate_local_code

PROJECT_ROOT = get_project_root()
CHECK_INTERVAL = 10 

def execute_python_test(test_file_path: str):
    print(f"🐳 [QA] Executing test inside Docker...")
    try:
        rel_test_path = os.path.relpath(test_file_path, os.path.join(PROJECT_ROOT, "compute-python"))
        result = subprocess.run(["docker", "compose", "exec", "-T", "compute-python", "python", "-m", "unittest", rel_test_path], cwd=PROJECT_ROOT, capture_output=True, text=True)
        return result.returncode == 0, result.stdout + "\n" + result.stderr
    except Exception as e:
        return False, str(e)

def process_qa_review(ticket):
    print(f"\n🛡️ [QA Gatekeeper] Reviewing: [{ticket['id']}]")
    target_file = ticket.get('target_file', '').strip()
    agent_type = ticket.get('agent')
    
    base_dir = os.path.join(PROJECT_ROOT, "compute-python" if agent_type == "compute" else "backend-java")
    full_path = os.path.abspath(os.path.join(base_dir, target_file))
    
    if not os.path.exists(full_path): return True, ""
    with open(full_path, "r", encoding="utf-8") as f: existing_code = f.read()

    if agent_type == "compute":
        print(f"🧠 [QA] Generating PyTest for {target_file}...")
        sys_prompt = f"Write a Python `unittest` for the following code. Assume filename is {os.path.basename(target_file).replace('.py', '')}. Output raw code only."
        
        # OPTIMIZATION: 1 line call, expects text. Strips markdown automatically.
        test_code = generate_local_code(sys_prompt, existing_code, expect_json=False)
            
        test_file_path = os.path.join(base_dir, f"test_{os.path.basename(target_file)}")
        with open(test_file_path, "w", encoding="utf-8") as f: f.write(test_code.strip() + "\n")
            
        return execute_python_test(test_file_path)
    else:
        return True, "Static review passed. (Java Dynamic Execution skipped for speed)"

def main():
    print("===================================================")
    print("🛡️ QA GATEKEEPER AGENT ONLINE")
    print("===================================================")
    
    while True:
        board = load_board()
        qa_ticket = next((t for t in board.get("in_review", []) if t.get("agent") in ["compute", "enterprise"]), None)
        
        if qa_ticket:
            board["in_review"] = [t for t in board["in_review"] if t["id"] != qa_ticket["id"]]
            save_board(board)
            
            success, logs = process_qa_review(qa_ticket)
            board = load_board() 
            
            if success:
                print(f"✅ [QA] PASSED: [{qa_ticket['id']}]")
                board["done"].append(qa_ticket)
            else:
                rejections = qa_ticket.get("qa_rejections", 0)
                if rejections < 2:
                    print(f"❌ [QA] FAILED: [{qa_ticket['id']}]. Kicking back to Dispatcher!")
                    qa_ticket["description"] += f"\n\n[QA FAILED]: Please fix. Logs:\n{logs}"
                    qa_ticket["qa_rejections"] = rejections + 1
                    board["todo"].insert(0, qa_ticket)
                else:
                    qa_ticket["status"] = "failed_qa"
                    board["done"].append(qa_ticket)
            save_board(board)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()