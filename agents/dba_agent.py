import os
import sys
import json
import time
import requests
import subprocess
from datetime import datetime

# Set up robust absolute paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BOARD_FILE = os.path.join(PROJECT_ROOT, "antigravity_board.json")

OLLAMA_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL = "qwen2.5-coder:7b"
CHECK_INTERVAL = 10 

def load_board():
    if not os.path.exists(BOARD_FILE):
        return {"todo": [], "in_progress": [], "in_review": [], "done": [], "archived": []}
    try:
        with open(BOARD_FILE, "r", encoding="utf-8") as f:
            board = json.load(f)
            for col in ["todo", "in_progress", "in_review", "done", "archived"]:
                if col not in board:
                    board[col] = []
            return board
    except Exception:
        return {"todo": [], "in_progress": [], "in_review": [], "done": [], "archived": []}

def save_board(board):
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=4)

def process_entity_migration(ticket):
    """Checks if the file is a JPA Entity, and if so, generates a Flyway SQL migration."""
    target_file = ticket.get('target_file', '').strip()
    
    # We only care about Java files
    if not target_file.endswith(".java"):
        return False

    full_path = os.path.abspath(os.path.join(PROJECT_ROOT, "backend-java", target_file))
    if not os.path.exists(full_path):
        return False

    with open(full_path, "r", encoding="utf-8") as f:
        java_code = f.read()

    # Check if this class is actually a database entity
    if "@Entity" not in java_code and "@Table" not in java_code:
        return False

    print(f"\n🗄️ [DBA Agent] Detected Data Model Change in: {os.path.basename(target_file)}")
    print(f"🧠 Spinning up 3070 Ti to generate PostgreSQL migration...")

    system_prompt = """
    You are an expert PostgreSQL Database Administrator and Data Architect.
    Your job is to read a Spring Boot Java JPA @Entity class and generate the corresponding SQL script to create or update its table.
    
    CRITICAL RULES:
    1. Use standard PostgreSQL syntax.
    2. Map Java UUID to PostgreSQL UUID, String to VARCHAR, Integer to INT, etc.
    3. Output ONLY the raw SQL commands. 
    4. Do NOT wrap the output in markdown backticks (like ```sql).
    5. Do NOT include any conversational text or explanations.
    """

    user_prompt = f"Generate the PostgreSQL CREATE TABLE or ALTER TABLE script for this JPA Entity:\n\n{java_code}"

    try:
        payload = {
            "model": LOCAL_MODEL,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 4000}
        }
        
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        sql_code = response.json().get("response", "").strip()
        
        # Strip markdown if hallucinated
        if sql_code.startswith("```"):
            lines = sql_code.split("\n")
            sql_code = "\n".join(lines[1:]) if len(lines) > 1 else sql_code
        if sql_code.endswith("```"):
            sql_code = sql_code[:-3]

        if not sql_code:
            print("⚠️ [DBA Agent] LLM returned empty SQL. Skipping.")
            return False

        # Prepare the Flyway migration directory
        migration_dir = os.path.join(PROJECT_ROOT, "backend-java", "src", "main", "resources", "db", "migration")
        os.makedirs(migration_dir, exist_ok=True)

        # Generate a unique Flyway version timestamp (e.g., V1715000000__Update_User.sql)
        class_name = os.path.basename(target_file).replace(".java", "")
        timestamp = int(datetime.now().timestamp())
        migration_filename = f"V{timestamp}__Update_{class_name}.sql"
        migration_path = os.path.join(migration_dir, migration_filename)

        with open(migration_path, "w", encoding="utf-8") as f:
            f.write(sql_code + "\n")

        print(f"✅ [DBA Agent] Successfully created migration script: {migration_filename}")
        
        # Trigger an immediate restart of the Enterprise backend so Flyway applies the DB changes
        print(f"🐳 [DBA Agent] Restarting backend-java to apply database schema updates...")
        subprocess.run(["docker", "compose", "build", "backend-java"], cwd=PROJECT_ROOT)
        subprocess.run(["docker", "compose", "up", "-d", "backend-java"], cwd=PROJECT_ROOT)

        return True

    except Exception as e:
        print(f"❌ [DBA Agent] Failed to generate SQL: {e}")
        return False

def main():
    print("===================================================")
    print("🗄️  DBA / DATA ARCHITECT AGENT ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Watching 'done' and 'archived' queues for JPA Entity changes...")
    print("===================================================")
    
    while True:
        board = load_board()
        updated = False
        
        # We check both done and archived columns in case the Refactor agent archived it before we saw it
        for column in ["done", "archived"]:
            for ticket in board.get(column, []):
                
                # Check if it's an enterprise ticket that we haven't processed yet
                if ticket.get("agent") == "enterprise" and not ticket.get("dba_processed"):
                    
                    # Process it (whether it results in a migration or not)
                    process_entity_migration(ticket)
                    
                    # Mark it as processed so we never look at it again
                    ticket["dba_processed"] = True
                    updated = True
        
        if updated:
            save_board(board)
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()