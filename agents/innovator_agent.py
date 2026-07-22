import os
import json
import time
import subprocess
import sys

# Set up robust absolute paths so this script works from ANY directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# Append current directory so we can use the local_llm adapter
sys.path.append(CURRENT_DIR)
try:
    from local_llm import generate_local_code
except ImportError:
    print("❌ Error: Could not import local_llm. Make sure local_llm.py is in the agents directory.")
    sys.exit(1)

BOARD_FILE = os.path.join(PROJECT_ROOT, "antigravity_board.json")
BLUEPRINT_FILE = os.path.join(CURRENT_DIR, "system_blueprint.json")
PO_AGENT_SCRIPT = os.path.join(CURRENT_DIR, "po_agent.py")
CHECK_INTERVAL = 15 # Check the board every 15 seconds

innovator_persona = """
You are an expert AI Chief Innovation Officer.
Your job is to read the system blueprint and current state, then invent ONE single, highly specific, and valuable new feature to add to the application.

You must output a strictly formatted JSON object containing:
1. "feature_request": A string describing the new feature in natural language as if a user was requesting it.
   Example: "Add a dark mode toggle to the top right of the dashboard navigation bar."
   
CRITICAL: Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
"""

def is_team_idle():
    """Checks if the kanban board has any pending or active tickets."""
    if not os.path.exists(BOARD_FILE):
        return True
    try:
        with open(BOARD_FILE, "r") as f:
            board = json.load(f)
            # Team is idle if both todo and in_progress are empty
            return len(board.get("todo", [])) == 0 and len(board.get("in_progress", [])) == 0
    except Exception:
        return True

def run_innovator_loop():
    print("===================================================")
    print("💡 INNOVATOR AGENT ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Watching the Kanban board. Will invent new features when the team is idle.")
    print("===================================================")
    
    while True:
        if is_team_idle():
            print("\n💤 [Innovator] Team is currently idle. Brainstorming a new feature...")
            
            system_blueprint = "{}"
            if os.path.exists(BLUEPRINT_FILE):
                with open(BLUEPRINT_FILE, "r", encoding="utf-8") as f:
                    system_blueprint = f.read()

            prompt = f"""
            The development team is idle. Based on this system blueprint, what is ONE small, iterative UI or Backend feature we should build next to improve the app?
            
            System Blueprint:
            {system_blueprint}
            """
            
            try:
                # Ask the local 3070 Ti to generate a feature idea
                generated_payload = generate_local_code(innovator_persona, prompt)
                feature_request = generated_payload.get("feature_request", "")
                
                if feature_request:
                    print(f"✨ [Innovator] Eureka! New Feature Idea: '{feature_request}'")
                    print("📫 [Innovator] Handing off to Product Owner Agent...")
                    
                    # Programmatically trigger the PO Agent using the absolute path and current python executable
                    subprocess.run([sys.executable, PO_AGENT_SCRIPT, feature_request])
                    
                    print("⏳ [Innovator] Idea delegated. Sleeping until team is idle again.")
                else:
                    print("⚠️ [Innovator] Failed to generate a valid feature request.")
            except Exception as e:
                print(f"❌ [Innovator] Brainstorming error: {e}")
                
        # Wait before checking the board again
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_innovator_loop()