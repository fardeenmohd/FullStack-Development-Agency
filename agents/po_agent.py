import os
import json
import sys
from agency_utils import load_board, save_board, get_project_root
from local_llm import generate_local_code

PROJECT_ROOT = get_project_root()
BLUEPRINT_FILE = os.path.join(PROJECT_ROOT, "system_blueprint.json")

po_persona = """
You are an expert Agile Product Owner and Technical Lead.
Your job is to take a user's high-level feature request and break it down into granular, actionable tickets for specialized AI developer agents.

You must output a strictly formatted JSON object containing:
1. "tickets": An array of objects, where each object represents a task.
   Each ticket object MUST have:
   - "id": A unique string ID (e.g., "UI-1", "API-1").
   - "agent": The specific agent to handle the task. Must be exactly one of: ["frontend", "compute", "enterprise", "devops", "qa"].
   - "target_file": The primary file this task will create or modify. CRITICAL: THIS MUST NEVER BE EMPTY.
   - "description": A highly detailed, technical prompt instructing exactly what code to write.
"""

def run_po_agent(user_prompt: str):
    print(f"📋 [Product Owner] Breaking down request: '{user_prompt}'")

    system_blueprint = "{}"
    if os.path.exists(BLUEPRINT_FILE):
        with open(BLUEPRINT_FILE, "r", encoding="utf-8") as f:
            system_blueprint = f.read()

    llm_prompt = f"""
    Current System Blueprint: {system_blueprint}
    User Feature Request: "{user_prompt}"
    """

    # OPTIMIZATION: One clean call to the local_llm adapter. 
    # It auto-retries if the JSON is malformed!
    generated_payload = generate_local_code(po_persona, llm_prompt, expect_json=True)
    new_tickets = generated_payload.get("tickets", [])
    
    if not new_tickets:
        print("⚠️ [PO] Did not return any tickets.")
        return

    # OPTIMIZATION: Clean board loading
    board = load_board()
        
    for ticket in new_tickets:
        # Safety Net
        target = ticket.get("target_file", "").strip()
        if not target or target in [".", "/", "\\"]:
            ticket["target_file"] = f"auto_generated_{ticket.get('id', 'task').lower()}.txt"
            
        board["todo"].append(ticket)
        print(f"  🎟️ Ticket Created: [{ticket['id']}] -> '{ticket['agent']}' for {ticket['target_file']}")
        
    save_board(board)
    print("\n✅ Backlog successfully updated! The Dispatcher can now pick up these tasks.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python po_agent.py \"Your feature request here\"")
    else:
        run_po_agent(sys.argv[1])