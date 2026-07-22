import os
import json
import time
import sys

# Set up robust absolute paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BOARD_FILE = os.path.join(PROJECT_ROOT, "antigravity_board.json")

# Append current directory so we can use the local_llm adapter
sys.path.append(CURRENT_DIR)
try:
    from local_llm import generate_local_code
except ImportError:
    print("❌ Error: Could not import local_llm. Make sure local_llm.py is in the agents directory.")
    sys.exit(1)

CHECK_INTERVAL = 10 # Poll every 10 seconds

secops_persona = """
You are an elite SecOps Engineer, Penetration Tester, and Code Auditor.
Your job is to read raw application code and ruthlessly hunt for security vulnerabilities.
Look for OWASP Top 10 issues: SQL injections, XSS, open CORS, CSRF, hardcoded secrets/passwords, insecure direct object references, or unsafe package imports.

You must output a strictly formatted JSON object containing:
1. "is_vulnerable": A boolean (true or false). Set to true ONLY if you find a legitimate, actionable security flaw. Ignore standard "best practices" or formatting issues; only flag actual vulnerabilities.
2. "bug_description": A string detailing the vulnerability and exact instructions on how to patch it. If is_vulnerable is false, leave this empty.

CRITICAL: Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
"""

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

def scan_file_for_vulnerabilities(ticket):
    """Reads the code file and sends it to the LLM for a security audit."""
    target_file = ticket.get('target_file', '').strip()
    agent_type = ticket.get('agent', 'compute')
    
    if not target_file:
        return False, ""

    base_dirs = {
        "frontend": os.path.join(PROJECT_ROOT, "frontend-nextjs"),
        "compute": os.path.join(PROJECT_ROOT, "compute-python"),
        "enterprise": os.path.join(PROJECT_ROOT, "backend-java"),
        "devops": PROJECT_ROOT,
        "qa": os.path.join(PROJECT_ROOT, "qa-tests")
    }
    
    base_dir = base_dirs.get(agent_type, PROJECT_ROOT)
    full_path = os.path.abspath(os.path.join(base_dir, target_file))
    
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        return False, ""

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            code_content = f.read()
    except Exception:
        return False, ""

    print(f"\n🕵️‍♂️ [SecOps] Auditing {os.path.basename(full_path)} for vulnerabilities...")

    user_prompt = f"""
    Analyze this file carefully for security flaws. Do not flag generic warnings, only clear vulnerabilities.
    
    File Path: {target_file}
    
    Code:
    {code_content}
    """

    try:
        response = generate_local_code(secops_persona, user_prompt)
        is_vulnerable = response.get("is_vulnerable", False)
        bug_description = response.get("bug_description", "")
        return is_vulnerable, bug_description
    except Exception as e:
        print(f"⚠️ [SecOps] Failed to audit {target_file}: {e}")
        return False, ""

def main():
    print("===================================================")
    print("🕵️‍♂️ SECOPS AGENT (THE HACKER) ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Scanning 'done' and 'archived' queues for insecure code...")
    print("===================================================")
    
    while True:
        board = load_board()
        board_updated = False
        
        # Check completed code for security flaws
        for column in ["done", "archived"]:
            for ticket in board.get(column, []):
                
                # Ignore failed tickets or tickets we've already audited
                if ticket.get("status") == "failed" or ticket.get("secops_scanned"):
                    continue
                
                # Mark as scanned so we don't get stuck in a loop
                ticket["secops_scanned"] = True
                board_updated = True
                
                # Perform the Audit
                is_vulnerable, bug_description = scan_file_for_vulnerabilities(ticket)
                
                if is_vulnerable and bug_description:
                    print(f"🚨 [SecOps] VULNERABILITY DETECTED IN {ticket.get('target_file')}!")
                    print(f"   Details: {bug_description[:100]}...")
                    
                    # ANTI-SPAM MEASURE: Check if a fix for this file is already queued
                    is_already_queued = False
                    for q_col in ["todo", "in_progress", "in_review"]:
                        for t in board.get(q_col, []):
                            if t.get("target_file") == ticket.get("target_file"):
                                is_already_queued = True
                                break
                        if is_already_queued:
                            break
                    
                    if not is_already_queued:
                        # Create a High-Priority Hotfix Ticket
                        hotfix_ticket = {
                            "id": f"SEC-BUG-{int(time.time())}",
                            "agent": ticket.get("agent"),
                            "target_file": ticket.get("target_file"),
                            "description": f"[URGENT SECURITY HOTFIX]\nThe SecOps Agent detected a critical vulnerability in this file:\n\n{bug_description}\n\nYou MUST rewrite the file completely to patch this security flaw while maintaining existing functionality.",
                            "retries": 0
                        }
                        
                        # Inject at index 0 so it's the very next thing the Dispatcher builds
                        board["todo"].insert(0, hotfix_ticket)
                        print(f"💉 [SecOps] Hotfix ticket [{hotfix_ticket['id']}] injected to the front of the Todo queue!")
                    else:
                        print(f"⚠️ [SecOps] A hotfix for {ticket.get('target_file')} is already in the pipeline. Skipping duplicate.")
                else:
                    print(f"✅ [SecOps] {os.path.basename(ticket.get('target_file', 'unknown'))} passed security audit.")

        if board_updated:
            save_board(board)
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()