import os
import json
import time
import requests
from datetime import datetime

# Set up robust absolute paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BOARD_FILE = os.path.join(PROJECT_ROOT, "antigravity_board.json")
CHANGELOG_FILE = os.path.join(PROJECT_ROOT, "CHANGELOG.md")

OLLAMA_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL = "qwen2.5-coder:7b"
CHECK_INTERVAL = 15  # Poll every 15 seconds

def load_board():
    """Loads the Kanban board state."""
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
    """Saves the Kanban board state."""
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=4)

def generate_changelog_entry(tickets):
    """Sends the completed tickets to the LLM to write a professional Changelog entry."""
    print(f"✍️  [Documenter] Drafting release notes for {len(tickets)} completed tickets...")
    
    # Format the tickets for the LLM context
    ticket_context = "\n\n".join(
        [f"Ticket ID: {t.get('id')}\nAgent: {t.get('agent')}\nFile: {t.get('target_file')}\nDescription: {t.get('description')}" 
         for t in tickets]
    )

    system_prompt = """
    You are an expert Technical Writer and Developer Advocate.
    Your job is to read a list of completed engineering tickets and write a professional, formatted Markdown CHANGELOG entry for a new release.
    
    CRITICAL RULES:
    1. Organize the notes logically (e.g., 🚀 Features, 🐛 Bug Fixes, 💅 UI/UX Polish, ⚙️ Backend/Infrastructure).
    2. Translate the highly technical ticket descriptions into user-friendly feature announcements.
    3. Include the Ticket IDs (e.g., [UI-1]) as reference tags at the end of bullet points.
    4. Output ONLY the raw Markdown content for this specific release. Do NOT wrap it in markdown code blocks.
    5. Do NOT include a top-level `# Changelog` title, as this will be appended to an existing file.
    """

    user_prompt = f"Here are the tickets completed in this sprint. Generate the release notes:\n\n{ticket_context}"

    try:
        payload = {
            "model": LOCAL_MODEL,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 3000}
        }
        
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        changelog_content = response.json().get("response", "").strip()
        
        # Strip markdown if hallucinated
        if changelog_content.startswith("```"):
            lines = changelog_content.split("\n")
            changelog_content = "\n".join(lines[1:]) if len(lines) > 1 else changelog_content
        if changelog_content.endswith("```"):
            changelog_content = changelog_content[:-3]

        return changelog_content

    except Exception as e:
        print(f"❌ [Documenter] Failed to generate Changelog entry: {e}")
        return None

def append_to_changelog(content):
    """Appends the generated Markdown to the root CHANGELOG.md file."""
    date_str = datetime.now().strftime("%B %d, %Y - %H:%M")
    version_id = f"v1.0.{int(time.time() / 10000)}" # Mock versioning based on timestamp
    
    header = f"\n\n## [{version_id}] - {date_str}\n\n"
    
    # Create file with a title if it doesn't exist
    if not os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write("# Project Antigravity - Autonomous Changelog\n")
            f.write("This file is automatically maintained by the AI Technical Writer Agent.\n")

    # Prepend new releases to the top (under the main header)
    with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
        existing_lines = f.readlines()
        
    # Find the insertion point (after the main title)
    insert_idx = 0
    for i, line in enumerate(existing_lines):
        if line.startswith("# "):
            insert_idx = i + 1
            # Skip any immediate sub-text
            while insert_idx < len(existing_lines) and not existing_lines[insert_idx].startswith("## "):
                insert_idx += 1
            break
            
    existing_lines.insert(insert_idx, header + content + "\n\n---\n")

    with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(existing_lines)
        
    print(f"✅ [Documenter] Successfully updated {CHANGELOG_FILE}!")

def main():
    print("===================================================")
    print("✍️  TECHNICAL WRITER AGENT ONLINE")
    print(f"📂 Bound to Project Root: {PROJECT_ROOT}")
    print("Watching 'archived' queue for undocumented tickets...")
    print("===================================================")
    
    while True:
        board = load_board()
        archived_tickets = board.get("archived", [])
        
        # Find all successfully completed tickets that haven't been documented yet
        undocumented_tickets = [
            t for t in archived_tickets 
            if not t.get("documented") and t.get("status") != "failed"
        ]
        
        if undocumented_tickets:
            # We have a batch to document!
            changelog_markdown = generate_changelog_entry(undocumented_tickets)
            
            if changelog_markdown:
                append_to_changelog(changelog_markdown)
                
                # Mark them all as documented
                for t in archived_tickets:
                    if t in undocumented_tickets:
                        t["documented"] = True
                
                # Save the board back
                board["archived"] = archived_tickets
                save_board(board)
            else:
                print("⚠️ [Documenter] Failed to get valid markdown, will try again next cycle.")
                
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()