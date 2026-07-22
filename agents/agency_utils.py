import os
import json
import re

def get_project_root():
    """Dynamically locates the root of the project from anywhere."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_board_path():
    return os.path.join(get_project_root(), "antigravity_board.json")

def load_board():
    """Loads the Kanban board safely and auto-heals missing columns."""
    board_file = get_board_path()
    default_board = {"todo": [], "in_progress": [], "in_review": [], "done": [], "archived": []}
    
    if not os.path.exists(board_file):
        return default_board
        
    try:
        with open(board_file, "r", encoding="utf-8") as f:
            board = json.load(f)
            # Auto-heal missing columns
            for col in default_board.keys():
                if col not in board:
                    board[col] = []
            return board
    except Exception:
        return default_board

def save_board(board):
    """Saves the Kanban board state."""
    with open(get_board_path(), "w", encoding="utf-8") as f:
        json.dump(board, f, indent=4)

def clean_llm_output(text: str) -> str:
    """Strips markdown formatting and backticks from LLM code/JSON outputs."""
    text = text.strip()
    if text.startswith("```"):
        # Remove the first line (e.g., ```python or ```json)
        text = re.sub(r"^```[a-zA-Z]*\n", "", text)
        if text.endswith("```"):
            text = text[:-3].strip()
    return text.strip()