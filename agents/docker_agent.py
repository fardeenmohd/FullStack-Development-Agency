import subprocess
import requests
import json
import re
import time
import os

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b" # Your local 3070 Ti model
MAX_BUILD_RETRIES = 3 
MAX_RUNTIME_RETRIES_PER_SERVICE = 3
CHECK_INTERVAL = 15 # How often to poll logs in Phase 2

# Set up robust absolute paths so this script works from ANY directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# Track retries so the AI doesn't get stuck in an infinite loop trying to fix the same runtime crash
service_retries = {}

def run_docker_build(service=None):
    """Runs docker compose build. If a specific service is provided, it only builds that one."""
    target = f" '{service}'" if service else " all containers"
    print(f"\n🚀 [Docker Agent] Running 'docker compose build'{target}...")
    
    cmd = ["docker", "compose", "build"]
    if service:
        cmd.append(service)
        
    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stdout + "\n" + e.stderr

def start_containers(service=None):
    """Starts the containers in detached mode."""
    cmd = ["docker", "compose", "up", "-d"]
    if service:
        cmd.append(service)
    subprocess.run(cmd, cwd=PROJECT_ROOT)

def ask_llm_for_fix(system_prompt, error_logs):
    """Sends the error logs to the local LLM and asks for a file fix using a dynamic prompt."""
    print("🧠 [Docker Agent] Analyzing logs with local AI...")
    
    # We only send the last 150 lines to avoid overflowing the LLM context window
    tail_logs = "\n".join(error_logs.splitlines()[-150:])
    
    prompt = f"""
    {system_prompt}
    
    ERROR LOGS:
    {tail_logs}
    
    You MUST respond using EXACTLY this format:
    
    FILE: <relative path to the file to fix, e.g., backend-java/pom.xml or compute-python/main.py>
    CONTENT:
    <the complete, fixed code for the file>
    END_CONTENT
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"❌ [Docker Agent] Failed to contact local LLM: {e}")
        return ""

def apply_fix(llm_response):
    """Parses the LLM response and overwrites the broken file."""
    file_match = re.search(r"FILE:\s*(.+)", llm_response)
    content_match = re.search(r"CONTENT:\n(.*?)\nEND_CONTENT", llm_response, re.DOTALL)

    if not file_match or not content_match:
        print("⚠️ [Docker Agent] LLM didn't return a properly formatted fix. Manual intervention required.")
        return False

    filepath = file_match.group(1).strip()
    new_content = content_match.group(1)

    full_path = os.path.join(PROJECT_ROOT, filepath)
    
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ [Docker Agent] Successfully applied AI fix to: {filepath}")
        return True
    except Exception as e:
        print(f"❌ [Docker Agent] Failed to write to file {filepath}: {e}")
        return False

def get_services():
    """Gets a list of all active services from the docker-compose file."""
    try:
        result = subprocess.run(
            ["docker", "compose", "config", "--services"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, check=True
        )
        return [s.strip() for s in result.stdout.splitlines() if s.strip()]
    except subprocess.CalledProcessError:
        return []

def get_recent_logs(service, lines=50):
    """Fetches the most recent logs for a specific service."""
    try:
        result = subprocess.run(
            ["docker", "compose", "logs", f"--tail={lines}", service],
            cwd=PROJECT_ROOT, capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def surveillance_loop():
    """Phase 2: Infinite loop monitoring live containers for runtime crashes."""
    print("\n===================================================")
    print("👁️  PHASE 2: RUNTIME SURVEILLANCE ONLINE")
    print("Listening for Tracebacks, Exceptions, and Crashes...")
    print("===================================================")
    
    error_signatures = ["Traceback (most recent call last):", "Exception:", "Error:", "ModuleNotFoundError", "SyntaxError"]
    
    while True:
        services = get_services()
        
        for service in services:
            logs = get_recent_logs(service, lines=30)
            
            # Check if any known error signatures are in the recent logs
            if any(sig.lower() in logs.lower() for sig in error_signatures):
                
                # Check circuit breaker
                retries = service_retries.get(service, 0)
                if retries >= MAX_RUNTIME_RETRIES_PER_SERVICE:
                    print(f"💀 [Surveillance] {service} keeps crashing. Max retries ({MAX_RUNTIME_RETRIES_PER_SERVICE}) reached. Manual intervention required.")
                    continue
                
                service_retries[service] = retries + 1
                print(f"\n🚨 [Surveillance] CRASH DETECTED in '{service}'! Dispatching to 3070 Ti...")
                
                # Ask LLM for runtime fix
                prompt = f"You are an expert Site Reliability Engineer (SRE). The Docker service '{service}' just crashed with a runtime error. Analyze the logs, identify the broken file, and provide the complete fixed code."
                llm_response = ask_llm_for_fix(prompt, logs)
                
                # Apply Fix & Hot-Restart
                if llm_response and apply_fix(llm_response):
                    print(f"🔄 [Surveillance] Hot-restarting {service}...")
                    run_docker_build(service)
                    start_containers(service)
                    
                    print("⏳ [Surveillance] Waiting 10 seconds for container to stabilize before resuming patrol...")
                    time.sleep(10)
                        
        time.sleep(CHECK_INTERVAL)

def main():
    print("===================================================")
    print("🤖 PHASE 1: AUTONOMOUS BUILD SUPERVISOR")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("===================================================")
    
    attempt = 1
    build_success = False
    
    while attempt <= MAX_BUILD_RETRIES:
        print(f"\n--- Build Attempt {attempt}/{MAX_BUILD_RETRIES} ---")
        
        success, logs = run_docker_build()
        
        if success:
            print("\n🎉 [Docker Agent] SUCCESS! All containers built without errors.")
            print("🚀 Starting the platform now...")
            start_containers()
            print("🌐 Access your platform at http://localhost:3000")
            build_success = True
            break
        else:
            print(f"❌ [Docker Agent] Build failed with errors.")
            
            prompt = "You are an expert DevOps and Software Engineer. The following Docker build just failed. Analyze the logs, identify the broken file, and provide the complete fixed code."
            llm_response = ask_llm_for_fix(prompt, logs)
            
            if llm_response:
                applied = apply_fix(llm_response)
                if not applied:
                    print("🛑 [Docker Agent] Stopping autonomous loop due to parsing error.")
                    break
            else:
                print("🛑 [Docker Agent] LLM returned empty response.Stopping.")
                break
                
            print("⏳ Waiting 3 seconds before retrying build...")
            time.sleep(3)
            attempt += 1

    if build_success:
        # Seamlessly transition into runtime surveillance
        surveillance_loop()
    else:
        print("\n💀 [Docker Agent] Max retries reached. The AI could not fix the build. Surveillance aborted.")

if __name__ == "__main__":
    main()