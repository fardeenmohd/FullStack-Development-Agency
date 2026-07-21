import os
import sys
import json
import time
import subprocess
import argparse

STATE_FILE = "pipeline_state.json"

# 🛠️ HYBRID PIPELINE CONFIGURATION 🛠️
# Tier 1: Cloud Architecture (Gemini 1.5 Pro)
# Tier 2: Factory Floor (Local RTX 3070 Ti)
PIPELINE = [
    {"key": "architect",  "script": "architect.py",        "name": "System Architect (Gemini)", "local": False},
    {"key": "frontend",   "script": "frontend_agent.py",   "name": "Frontend Specialist (Local)", "local": True},
    {"key": "compute",    "script": "compute_agent.py",    "name": "Compute Scientist (Local)", "local": True},
    {"key": "enterprise", "script": "enterprise_agent.py", "name": "Enterprise Engineer (Local)", "local": True},
    {"key": "qa",         "script": "qa_agent.py",         "name": "QA Gatekeeper (Local)", "local": True},
    {"key": "devops",     "script": "devops_agent.py",     "name": "DevOps Architect (Local)", "local": True}
]

def load_state():
    if not os.path.exists(STATE_FILE):
        return {step["key"]: False for step in PIPELINE}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def run_agent_script(script_name: str):
    """Executes the agent script using the current virtual environment's Python."""
    result = subprocess.run([sys.executable, script_name])
    return result.returncode == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hybrid AI Agent Factory Orchestrator")
    parser.add_argument("--reset", action="store_true", help="Reset the pipeline state to start over")
    parser.add_argument("--skip-architect", action="store_true", help="Skip Gemini to preserve the current system_blueprint.json")
    args = parser.parse_args()

    print("🤖 Hybrid Agent Factory Orchestrator Booting Up...")
    
    state = load_state()
    
    if args.reset:
        print(f"🔄 Resetting pipeline state...")
        state = {step["key"]: False for step in PIPELINE}
        save_state(state)
        
    if args.skip_architect:
        print(f"⏭️ Skipping Architect. Preserving current system_blueprint.json...")
        state["architect"] = True
        save_state(state)

    while True:
        state = load_state()
        all_completed = True
        
        for step in PIPELINE:
            if not state.get(step["key"]):
                all_completed = False
                print(f"\n▶️ Starting pipeline step: {step['name']}")
                
                success = run_agent_script(step["script"])
                
                if success:
                    print(f"✅ {step['name']} completed successfully!")
                    state[step["key"]] = True
                    save_state(state)
                else:
                    print(f"❌ {step['name']} encountered an error.")
                    if not step["local"]:
                        print(f"💤 API Error. Orchestrator sleeping for 60 seconds before retrying Gemini...")
                        time.sleep(60)
                    else:
                        print(f"⚠️ Local generation failed. Check your Ollama server/script and try again.")
                        sys.exit(1) # We exit immediately on local errors because it's usually a script bug, not a timeout
                    break # Break the FOR loop to restart the WHILE loop and retry
        
        if all_completed:
            print("\n🏁 [SUCCESS] The Hybrid Factory has completed all stages!")
            print("🐳 Your project is ready! Run: docker compose up --build")
            break