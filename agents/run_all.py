import json
import time
import os
from agents.antigravity_client import delegate_to_cloud

BOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "antigravity_board.json")
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def load_board():
    with open(BOARD_FILE, "r") as f:
        return json.load(f)

def save_board(board):
    with open(BOARD_FILE, "w") as f:
        json.dump(board, f, indent=4)

def run_dispatcher():
    print("🚀 [Cloud Dispatcher] Online. Scanning for 'todo' tickets...")
    
    while True:
        board = load_board()
        
        if len(board["todo"]) > 0:
            # Grab the first ticket
            ticket = board["todo"].pop(0)
            target_file = ticket["target_file"]
            description = ticket["description"]
            
            print(f"\n📥 [Cloud Dispatcher] Picked up ticket: {ticket['id']} -> {target_file}")
            
            # Read existing code if it exists
            full_path = os.path.join(PROJECT_ROOT, target_file)
            existing_code = ""
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    existing_code = f.read()

            # ☁️ THE MAGIC: Send it to Google's Cloud Sandbox instead of Local GPU!
            new_code = delegate_to_cloud(description, target_file, existing_code)
            
            if new_code:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Auto-Fixer for Next.js imports (The fix we discussed earlier)
                if target_file.endswith(('.tsx', '.jsx')):
                    if 'useEffect' in new_code and 'import { useEffect' not in new_code:
                        new_code = "import { useEffect } from 'react';\n" + new_code
                    if 'useState' in new_code and 'import { useState' not in new_code:
                        new_code = "import { useState } from 'react';\n" + new_code
                
                # Write the cloud-generated code locally
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(new_code)
                print(f"✅ [Cloud Dispatcher] Google Antigravity finished writing {target_file}!")
                
                # Move to Review
                board["in_review"].append(ticket)
            else:
                print(f"⚠️ [Cloud Dispatcher] Cloud task failed. Returning to Todo.")
                ticket["retries"] = ticket.get("retries", 0) + 1
                board["todo"].append(ticket)
            
            save_board(board)
            time.sleep(2) # Brief pause before the next ticket
            
        else:
            # No tickets, sleep for 5 seconds
            time.sleep(5)

if __name__ == "__main__":
    run_dispatcher()