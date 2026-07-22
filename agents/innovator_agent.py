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
BLUEPRINT_FILE = os.path.join(PROJECT_ROOT, "system_blueprint.json")
HISTORY_FILE = os.path.join(PROJECT_ROOT, "innovation_history.txt")
PO_AGENT_SCRIPT = os.path.join(CURRENT_DIR, "po_agent.py")
CHECK_INTERVAL = 15 # Check the board every 15 seconds

innovator_persona = """
You are an expert AI Chief Innovation Officer and Product Strategist.
Your job is to read the system blueprint and review the history of previously implemented features. 
You must ensure that any new feature you invent is in perfect sync with existing features, creates synergy, and cohesively builds upon the established application ecosystem.

You can either:
A) Invent ONE new, synergistic feature that fits perfectly with the current app.
B) Suggest ONE major upgrade or refinement to an existing feature from the history to make it more robust.

You must output a strictly formatted JSON object containing:
1. "feature_request": A string describing the new feature or upgrade in natural language as if a user was requesting it.
   Example: "Upgrade the existing dark mode feature by saving the user's preference in localStorage and auto-matching the OS default."
   
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

def get_innovation_history():
    """Reads the history of previously generated features."""
    if not os.path.exists(HISTORY_FILE):
        return "No features have been implemented yet."
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = f.read().strip()
            return history if history else "No features have been implemented yet."
    except Exception:
        return "Could not read history."

def append_to_history(feature_request):
    """Saves the newly generated feature to the history file."""
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"- {feature_request}\n")
    except Exception as e:
        print(f"⚠️ [Innovator] Could not write to history file: {e}")

def run_innovator_loop():
    print("===================================================")
    print("💡 INNOVATOR AGENT ONLINE (Now with Long-Term Memory 🧠)")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Watching the Kanban board. Will invent new features when the team is idle.")
    print("===================================================")
    
    while True:
        if is_team_idle():
            print("\n💤 [Innovator] Team is currently idle. Brainstorming a cohesive new feature...")
            
            system_blueprint = "{}"
            if os.path.exists(BLUEPRINT_FILE):
                with open(BLUEPRINT_FILE, "r", encoding="utf-8") as f:
                    system_blueprint = f.read()

            history_text = get_innovation_history()

            prompt = f"""
            The development team is idle. Review the system blueprint and the history of existing features below.
            
            System Blueprint:
            {system_blueprint}
            
            EXISTING APP CAPABILITIES (History of completed features):
            {history_text}
            
            Task: Propose ONE small, iterative UI or Backend feature. It must either cohesively expand/upgrade the EXISTING APP CAPABILITIES or introduce a new synergistic feature that aligns perfectly with what we have already built. Do not suggest an exact duplicate of what exists, but rather a logical next step.
            """
            
            try:
                # Ask the local 3070 Ti to generate a feature idea
                generated_payload = generate_local_code(innovator_persona, prompt)
                feature_request = generated_payload.get("feature_request", "")
                
                if feature_request:
                    print(f"✨ [Innovator] Eureka! New Feature Idea: '{feature_request}'")
                    
                    # Save to memory so it doesn't suggest it again
                    append_to_history(feature_request)
                    
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