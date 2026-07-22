import subprocess
import os
import time
import sys

# List of all your agency scripts with their desired terminal window titles
AGENTS = [
    ("1 - Innovator & PO", "agents/innovator_agent.py"),
    ("2 - Dispatcher", "agents/run_all.py"),
    ("3 - UX/UI Designer", "agents/designer_agent.py"),
    ("4 - QA Gatekeeper", "agents/qa_gatekeeper.py"),
    ("5 - SecOps Hacker", "agents/secops_agent.py"),
    ("6 - DBA Data Architect", "agents/dba_agent.py"),
    ("7 - Docker SRE", "agents/docker_agent.py"),
    ("8 - Refactor Agent", "agents/refactor_agent.py"),
    ("9 - Technical Writer", "agents/documenter_agent.py")
]

# Adjust 'venv' below if your virtual environment folder is named '.venv' or 'env'
VENV_NAME = "venv"
VENV_ACTIVATION_CMD = f"source agents/{VENV_NAME}/Scripts/activate"

# Standard installation path for Git Bash on Windows
GIT_BASH_PATH = r"C:\Program Files\Git\git-bash.exe"

def main():
    if not os.path.exists(GIT_BASH_PATH):
        print(f"❌ Error: Git Bash not found at '{GIT_BASH_PATH}'.")
        print("💡 Hint: If you installed Git Bash somewhere else, please update the GIT_BASH_PATH variable inside this script.")
        sys.exit(1)

    # Get the absolute path of the project root to ensure Git Bash starts in the right place
    project_root = os.path.abspath(os.path.dirname(__file__))
    # Convert Windows backslashes to forward slashes for Git Bash compatibility
    bash_root_path = project_root.replace('\\', '/')

    print("===================================================")
    print("🚀 BOOTING UP AUTONOMOUS AI SOFTWARE AGENCY")
    print("===================================================")

    for name, script in AGENTS:
        print(f"👔 Spawning terminal for: {name}...")
        
        # The bash command does 4 things:
        # 1. Changes directory to the absolute project root
        # 2. Uses ANSI escape codes (\033]0;TITLE\007) to set the window title
        # 3. Activates the Python virtual environment
        # 4. Runs the script, and if it crashes/stops, it uses 'read' to keep the window open so you can read the error logs!
        bash_command = (
            f"cd '{bash_root_path}'; "
            f"echo -ne '\\033]0;{name}\\007'; "
            f"{VENV_ACTIVATION_CMD}; "
            f"python {script}; "
            f"echo ''; echo '🛑 Process ended or crashed. Press Enter to close this window...'; read"
        )
        
        try:
            subprocess.Popen([GIT_BASH_PATH, "-c", bash_command])
        except Exception as e:
            print(f"❌ Failed to launch {name}: {e}")
            
        # A slight delay prevents Windows from stacking the windows completely on top of each other
        # and gives the OS time to properly spawn the processes
        time.sleep(0.5) 

    print("\n✅ All 9 agents have been successfully dispatched!")
    print("💼 You can now sit back and watch your company work.")

if __name__ == "__main__":
    main()