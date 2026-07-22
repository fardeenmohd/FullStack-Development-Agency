import subprocess
import requests
import json
import re
import time
import os

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"
PROJECT_ROOT = ".." # Script runs from inside the 'agents' folder
CHECK_INTERVAL = 15 # How often to poll the logs (in seconds)
MAX_RETRIES_PER_SERVICE = 3

# We track retries so the AI doesn't get stuck in an infinite loop trying to fix the same container
service_retries = {}

def get_services():
    """Gets a list of all services in the docker-compose file."""
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

def restart_service(service):
    """Rebuilds and restarts a specific service after a fix is applied."""
    print(f"🔄 [Surveillance] Rebuilding and restarting {service}...")
    subprocess.run(["docker", "compose", "build", service], cwd=PROJECT_ROOT)
    subprocess.run(["docker", "compose", "up", "-d", service], cwd=PROJECT_ROOT)
    print(f"✅ [Surveillance] {service} is back online!")

def analyze_runtime_error(service, logs):
    """Sends runtime logs to the local LLM for a hotfix."""
    print(f"🚨 [Surveillance] CRASH DETECTED in '{service}'! Dispatching to 3070 Ti...")
    
    prompt = f"""
    You are an expert Site Reliability Engineer (SRE). 
    The following Docker service '{service}' just crashed with a runtime error. 
    Analyze the logs, identify the broken file, and provide the complete fixed code.
    
    RUNTIME LOGS:
    {logs}
    
    You MUST respond using EXACTLY this format:
    
    FILE: <relative path to the file to fix, e.g., compute-python/main.py or compute-python/requirements.txt>
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
        print(f"❌ [Surveillance] Failed to contact local LLM: {e}")
        return ""

def apply_hotfix(llm_response):
    """Parses the LLM response and applies the patch to the live file."""
    file_match = re.search(r"FILE:\s*(.+)", llm_response)
    content_match = re.search(r"CONTENT:\n(.*?)\nEND_CONTENT", llm_response, re.DOTALL)

    if not file_match or not content_match:
        print("⚠️ [Surveillance] LLM didn't return a properly formatted fix.")
        return False

    filepath = file_match.group(1).strip()
    new_content = content_match.group(1)

    full_path = os.path.join(PROJECT_ROOT, filepath)
    
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"🩹 [Surveillance] Hotfix applied successfully to: {filepath}")
        return True
    except Exception as e:
        print(f"❌ [Surveillance] Failed to write hotfix to {filepath}: {e}")
        return False

def main():
    print("===================================================")
    print("👁️  RUNTIME SURVEILLANCE AGENT ONLINE")
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
                if retries >= MAX_RETRIES_PER_SERVICE:
                    print(f"💀 [Surveillance] {service} keeps crashing. Max retries ({MAX_RETRIES_PER_SERVICE}) reached. Manual intervention required.")
                    continue
                
                service_retries[service] = retries + 1
                
                # Step 1: Get Fix
                llm_response = analyze_runtime_error(service, logs)
                
                # Step 2: Apply Fix
                if llm_response:
                    if apply_hotfix(llm_response):
                        # Step 3: Hot-Restart the specific container
                        restart_service(service)
                        
                        # Clear logs temporarily by waiting so we don't double-trigger on the same old error message
                        print("⏳ [Surveillance] Waiting 10 seconds for container to stabilize...")
                        time.sleep(10)
                        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()