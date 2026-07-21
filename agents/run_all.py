import os
import sys
import json
import time
import subprocess

STATE_FILE = "pipeline_state.json"

# Initialize state if it doesn't exist
if not os.path.exists(STATE_FILE):
    initial_state = {
        "architect": True,        
        "synthesizer": True,      
        "frontend": True,         
        "compute": True,          
        "enterprise": True,       # Marked True since this step successfully finished!
        "qa_gatekeeper": False,   
        "devops": False           
    }
    with open(STATE_FILE, "w") as f:
        json.dump(initial_state, f, indent=4)

def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def run_agent_script(script_name: str, step_key: str):
    state = load_state()
    
    if state.get(step_key):
        print(f"⏭️ Skipping {script_name} - already marked as COMPLETED.")
        return True

    print(f"\n▶️ Starting pipeline step: {script_name}")
    
    # sys.executable ensures the background process stays locked inside your virtual environment
    result = subprocess.run([sys.executable, script_name])
    
    if result.returncode == 0:
        print(f"✅ {script_name} completed successfully!")
        state[step_key] = True
        save_state(state)
        return True
    else:
        print(f"❌ {script_name} encountered an error or was interrupted.")
        return False

if __name__ == "__main__":
    print("🤖 Agent Factory Orchestrator Booting Up...")
    
    while True:
        state = load_state()
        
        # 1. Verification Safety Check: Enterprise Agent
        if not state.get("enterprise"):
            print("\n⏳ Attempting to run Enterprise Agent...")
            if not run_agent_script("enterprise_agent.py", "enterprise"):
                print("💤 Orchestrator sleeping for 5 minutes before retrying Enterprise...")
                time.sleep(300)
                continue 
                
        # 2. Run QA Gatekeeper (Currently fighting through 503 errors)
        if not state.get("qa_gatekeeper"):
            print("\n⏳ Attempting to run QA Gatekeeper...")
            if not run_agent_script("qa_agent.py", "qa_gatekeeper"):
                print("💤 Server down or quota limit hit. Orchestrator sleeping for 5 minutes before retrying QA...")
                time.sleep(300)
                continue # Loop back and try QA again after the cooldown
                
        # 3. Run DevOps Architect
        if not state.get("devops"):
            print("\n⏳ Attempting to run DevOps Architect...")
            if not run_agent_script("devops_agent.py", "devops"):
                print("💤 Orchestrator sleeping for 5 minutes before retrying DevOps...")
                time.sleep(300)
                continue # Loop back and try DevOps again if it hits a server bump
                
        # Final Verification Gate
        if state.get("enterprise") and state.get("qa_gatekeeper") and state.get("devops"):
            print("\n🏁 [SUCCESS] The pipeline has completed all stages successfully!")
            print("📁 All directories populated: frontend-nextjs, compute-python, backend-java, qa-tests, and root docker files.")
            break