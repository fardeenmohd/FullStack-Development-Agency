import os
import time
from datetime import datetime
from agency_utils import load_board, save_board, get_project_root
from local_llm import generate_local_code

PROJECT_ROOT = get_project_root()
CHANGELOG_FILE = os.path.join(PROJECT_ROOT, "CHANGELOG.md")
CHECK_INTERVAL = 15

def generate_changelog_entry(tickets):
    print(f"✍️  [Documenter] Drafting release notes for {len(tickets)} completed tickets...")
    ticket_context = "\n\n".join([f"Ticket ID: {t.get('id')}\nAgent: {t.get('agent')}\nDescription: {t.get('description')}" for t in tickets])

    sys_prompt = "You are an expert Technical Writer. Read engineering tickets and write a Markdown CHANGELOG entry for a new release. Output raw Markdown text only."
    user_prompt = f"Generate release notes for these tickets:\n\n{ticket_context}"

    # OPTIMIZATION: 1 line call, expects text
    return generate_local_code(sys_prompt, user_prompt, expect_json=False)

def append_to_changelog(content):
    date_str = datetime.now().strftime("%B %d, %Y - %H:%M")
    version_id = f"v1.0.{int(time.time() / 10000)}" 
    header = f"\n\n## [{version_id}] - {date_str}\n\n"
    
    if not os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write("# Project Antigravity - Autonomous Changelog\n")

    with open(CHANGELOG_FILE, "r", encoding="utf-8") as f: existing_lines = f.readlines()
        
    insert_idx = next((i + 1 for i, line in enumerate(existing_lines) if line.startswith("# ")), len(existing_lines))
    while insert_idx < len(existing_lines) and not existing_lines[insert_idx].startswith("## "): insert_idx += 1
            
    existing_lines.insert(insert_idx, header + content + "\n\n---\n")

    with open(CHANGELOG_FILE, "w", encoding="utf-8") as f: f.writelines(existing_lines)
    print(f"✅ [Documenter] Updated {os.path.basename(CHANGELOG_FILE)}!")

def main():
    print("===================================================")
    print("✍️  TECHNICAL WRITER AGENT ONLINE")
    print("===================================================")
    
    while True:
        board = load_board()
        archived_tickets = board.get("archived", [])
        
        undocumented = [t for t in archived_tickets if not t.get("documented") and t.get("status") != "failed"]
        
        if undocumented:
            changelog_markdown = generate_changelog_entry(undocumented)
            if changelog_markdown:
                append_to_changelog(changelog_markdown)
                for t in archived_tickets:
                    if t in undocumented: t["documented"] = True
                save_board(board)
                
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()