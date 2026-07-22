import os
import json
import sys
from local_llm import generate_local_code

BOARD_FILE = "./antigravity_board.json"

po_persona = """
You are an expert Agile Product Owner and Technical Lead.
Your job is to take a user's high-level feature request and break it down into granular, actionable tickets for specialized AI developer agents.

You must output a strictly formatted JSON object containing:
1. "tickets": An array of objects, where each object represents a task.
   Each ticket object MUST have:
   - "id": A unique string ID (e.g., "UI-1", "API-1").
   - "agent": The specific agent to handle the task. Must be exactly one of: ["frontend", "compute", "enterprise", "devops", "qa"].
   - "target_file": The primary file this task will create or modify (e.g., "app/page.tsx" or "main.py").
   - "description": A highly detailed, technical prompt that will be sent to the developer agent instructing them exactly what code to write.

CRITICAL: Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
"""

def init_board():
    """Initializes the Antigravity board if it doesn't exist."""
    if not os.path.exists(BOARD_FILE):
        with open(BOARD_FILE, "w") as f:
            json.dump({"todo": [], "in_progress": [], "done": []}, f, indent=4)

def run_po_agent(user_prompt: str):
    init_board()
    
    print(f"📋 Product Owner Agent is breaking down request: '{user_prompt}'")

    system_blueprint = "{}"
    if os.path.exists("system_blueprint.json"):
        with open("system_blueprint.json", "r", encoding="utf-8") as f:
            system_blueprint = f.read()

    llm_prompt = f"""
    Current System Architecture Blueprint:
    {system_blueprint}
    
    User Feature Request:
    "{user_prompt}"
    
    Break this request down into technical tickets. 
    If the user asks for a UI dashboard, assign a ticket to the "frontend" agent to overwrite "app/page.tsx" with a modern Tailwind CSS dashboard.
    """

    try:
        # Ask the local 3070 Ti to generate the tickets
        generated_payload = generate_local_code(po_persona, llm_prompt)
        new_tickets = generated_payload.get("tickets", [])
        
        if not new_tickets:
            print("⚠️ PO Agent did not return any tickets.")
            return

        # Load the current board
        with open(BOARD_FILE, "r") as f:
            board = json.load(f)
            
        # Append new tickets to the 'todo' column
        for ticket in new_tickets:
            board["todo"].append(ticket)
            print(f"  🎟️ Ticket Created: [{ticket['id']}] -> Assigned to '{ticket['agent']}' for {ticket['target_file']}")
            
        # Save the updated board
        with open(BOARD_FILE, "w") as f:
            json.dump(board, f, indent=4)
            
        print("\n✅ Backlog successfully updated! The Antigravity Dispatcher can now pick up these tasks.")

    except Exception as e:
        print(f"❌ Error during PO ticket generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python po_agent.py \"Your feature request here\"")
    else:
        request = sys.argv[1]
        run_po_agent(request)