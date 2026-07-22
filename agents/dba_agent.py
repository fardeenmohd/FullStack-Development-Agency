import os
import time
import subprocess
from datetime import datetime
from agency_utils import load_board, save_board, get_project_root
from local_llm import generate_local_code

PROJECT_ROOT = get_project_root()
CHECK_INTERVAL = 10 

def process_entity_migration(ticket):
    target_file = ticket.get('target_file', '').strip()
    if not target_file.endswith(".java"): return False

    full_path = os.path.abspath(os.path.join(PROJECT_ROOT, "backend-java", target_file))
    if not os.path.exists(full_path): return False
    with open(full_path, "r", encoding="utf-8") as f: java_code = f.read()
    if "@Entity" not in java_code and "@Table" not in java_code: return False

    print(f"\n🗄️ [DBA Agent] Detected Data Model Change in: {os.path.basename(target_file)}")

    sys_prompt = "You are a PostgreSQL DBA. Read a Java JPA @Entity class and generate the CREATE/ALTER TABLE SQL script. Output raw SQL only."
    user_prompt = f"Generate PostgreSQL script for this JPA Entity:\n\n{java_code}"

    # OPTIMIZATION: 1 line call, expects raw SQL text
    sql_code = generate_local_code(sys_prompt, user_prompt, expect_json=False)

    if not sql_code: return False

    migration_dir = os.path.join(PROJECT_ROOT, "backend-java", "src", "main", "resources", "db", "migration")
    os.makedirs(migration_dir, exist_ok=True)
    
    timestamp = int(datetime.now().timestamp())
    filename = f"V{timestamp}__Update_{os.path.basename(target_file).replace('.java', '')}.sql"
    
    with open(os.path.join(migration_dir, filename), "w", encoding="utf-8") as f: f.write(sql_code + "\n")

    print(f"✅ [DBA] Generated migration: {filename}")
    subprocess.run(["docker", "compose", "build", "backend-java"], cwd=PROJECT_ROOT)
    subprocess.run(["docker", "compose", "up", "-d", "backend-java"], cwd=PROJECT_ROOT)
    return True

def main():
    print("===================================================")
    print("🗄️  DBA / DATA ARCHITECT AGENT ONLINE")
    print("===================================================")
    
    while True:
        board = load_board()
        updated = False
        
        for column in ["done", "archived"]:
            for ticket in board.get(column, []):
                if ticket.get("agent") == "enterprise" and not ticket.get("dba_processed"):
                    process_entity_migration(ticket)
                    ticket["dba_processed"] = True
                    updated = True
        
        if updated: save_board(board)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()