import os
import time
from agency_utils import load_board, save_board, get_project_root
from local_llm import generate_local_code

PROJECT_ROOT = get_project_root()
CHECK_INTERVAL = 10 

secops_persona = """
You are an elite SecOps Engineer.
Analyze raw code for OWASP Top 10 vulnerabilities (SQL injections, hardcoded passwords).
Output JSON: {"is_vulnerable": bool, "bug_description": string}
"""

def scan_file_for_vulnerabilities(ticket):
    target_file = ticket.get('target_file', '').strip()
    agent_type = ticket.get('agent', 'compute')
    
    base_dirs = {
        "frontend": "frontend-nextjs", "compute": "compute-python",
        "enterprise": "backend-java", "devops": "", "qa": "qa-tests"
    }
    
    full_path = os.path.abspath(os.path.join(PROJECT_ROOT, base_dirs.get(agent_type, ""), target_file))
    
    if not os.path.exists(full_path) or not os.path.isfile(full_path): return False, ""
    with open(full_path, "r", encoding="utf-8") as f: code_content = f.read()

    print(f"\n🕵️‍♂️ [SecOps] Auditing {os.path.basename(full_path)}...")
    
    # OPTIMIZATION: 1 line call, expects JSON.
    response = generate_local_code(secops_persona, f"File: {target_file}\nCode:\n{code_content}", expect_json=True)
    return response.get("is_vulnerable", False), response.get("bug_description", "")

def main():
    print("===================================================")
    print("🕵️‍♂️ SECOPS AGENT (THE HACKER) ONLINE")
    print("===================================================")
    
    while True:
        board = load_board()
        board_updated = False
        
        for column in ["done", "archived"]:
            for ticket in board.get(column, []):
                if ticket.get("status") == "failed" or ticket.get("secops_scanned"): continue
                
                ticket["secops_scanned"] = True
                board_updated = True
                
                is_vulnerable, bug_description = scan_file_for_vulnerabilities(ticket)
                
                if is_vulnerable and bug_description:
                    print(f"🚨 [SecOps] VULNERABILITY DETECTED IN {ticket.get('target_file')}!")
                    
                    # Prevent duplicate spam by checking active queues
                    is_already_queued = any(t.get("target_file") == ticket.get("target_file") for col in ["todo", "in_progress", "in_review"] for t in board.get(col, []))
                    
                    if not is_already_queued:
                        board["todo"].insert(0, {
                            "id": f"SEC-{int(time.time())}",
                            "agent": ticket.get("agent"),
                            "target_file": ticket.get("target_file"),
                            "description": f"[URGENT SEC HOTFIX]\n{bug_description}\nRewrite completely to patch.",
                            "retries": 0
                        })
                else:
                    print(f"✅ [SecOps] {os.path.basename(ticket.get('target_file'))} passed.")

        if board_updated: save_board(board)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()