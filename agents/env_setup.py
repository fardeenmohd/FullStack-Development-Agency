import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ Error: python-dotenv is not installed. Please run: pip install python-dotenv")
    sys.exit(1)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

# This will inject the variables from the .env file into the system's environment
load_dotenv(dotenv_path=ENV_PATH)

def get_gemini_key() -> str:
    """
    Safely retrieves the Gemini API key from the environment.
    """
    key = os.getenv("GEMINI_API_KEY")
    
    if not key or key == "your_gemini_api_key_here":
        print("⚠️  Warning: GEMINI_API_KEY is not set correctly in your .env file.")
        print("💡 Hint: Open the .env file in the root of your project and paste your actual key.")
        return ""
        
    return key

# Optional: Run a quick test if executed directly
if __name__ == "__main__":
    test_key = get_gemini_key()
    if test_key:
        print("✅ Environment successfully loaded! Key is ready to use.")