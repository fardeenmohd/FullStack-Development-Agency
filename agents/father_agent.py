import os
import sys
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def run_father_agent():
    print("\n🧐 FATHER AGENT (The Critic) Booting Up...")
    
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        print(f"❌ Error: '{req_file}' not found. Mother Agent must run first.")
        sys.exit(1)

    with open(req_file, "r", encoding="utf-8") as f:
        master_spec = f.read()

    print("🔍 Reviewing Mother's Master Specification for logical gaps...")

    prompt = f"""
    You are an elite Lead Systems Reviewer (The Father Agent).
    Your job is to critically analyze the following Master Requirements Document created by the CTO (The Mother Agent).
    
    You are looking for:
    1. Missing Data Models (e.g., A feature is mentioned, but where is the data stored?)
    2. Broken User Flows (e.g., A user can create an item, but how do they delete it?)
    3. Missing API Endpoints (e.g., The frontend needs data that the backend isn't exposing).
    4. Unrealistic or vague assumptions.
    
    If the document is perfect, output exactly: "APPROVED".
    If there are flaws, write a concise, strict bulleted list of necessary fixes. Do NOT rewrite the document yourself; just provide the feedback.
    
    Document to Review:
    {master_spec}
    """

    try:
        response = client.models.generate_content(
            model='gemini-1.5-pro', # Pro model for critical reasoning
            contents=prompt
        )
        
        feedback = response.text.strip()
        
        if "APPROVED" in feedback.upper() and len(feedback) < 20:
            print("✅ Father Agent: The specification is flawless. Approved for architecture.")
            return True
        else:
            with open("feedback.txt", "w", encoding="utf-8") as f:
                f.write(feedback)
            print("❌ Father Agent: Found structural flaws! Sent feedback back to Mother.")
            return False
            
    except Exception as e:
        print(f"❌ Error during Father Agent review: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_father_agent()