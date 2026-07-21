import os
import sys
import subprocess
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def run_mother_agent(idea=None, feedback=None):
    print("\n👑 MOTHER AGENT (The Visionary) is active...")
    
    if feedback:
        print("🧠 Mother Agent is revising the specification based on Father's feedback...")
        prompt = f"""
        You are an elite Chief Technology Officer (CTO). 
        You previously wrote a Master Requirements Document for: "{idea}"
        
        The Lead Systems Reviewer (Father Agent) found flaws and provided the following feedback:
        {feedback}
        
        Rewrite the ENTIRE Master Requirements Document, explicitly fixing every issue mentioned in the feedback.
        Maintain the high level of detail for Features, Data Models, and API Endpoints.
        """
    else:
        print("🧠 Mother Agent is designing the initial master specification...")
        prompt = f"""
        You are an elite Chief Technology Officer (CTO).
        The user wants to build the following software platform: "{idea}"
        
        Write a comprehensive, highly detailed Master Requirements Document for this system.
        Include:
        1. Core Features & Business Logic
        2. Primary User Flows
        3. Recommended Database Entities (Users, Items, Transactions, etc.)
        4. Key API Endpoints needed
        
        Do NOT write code. Write a pure technical specification that an AI System Architect can read to generate a blueprint.
        """
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-pro', 
            contents=prompt
        )
        
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print("✅ Mother Agent: Specification updated and saved to 'requirements.txt'")
        
    except Exception as e:
        print(f"❌ Error generating specs: {e}")
        sys.exit(1)

def run_parent_loop():
    print("=========================================")
    print("      THE PARENTAL GUIDANCE SYSTEM       ")
    print("=========================================")
    idea = input("\n💡 What is your new startup idea?\n> ")

    # Step 1: Initial Draft
    run_mother_agent(idea=idea)
    
    # The Loop: Father reviews, Mother revises (Max 3 iterations to prevent infinite loops)
    for iteration in range(3):
        time.sleep(2) # Brief pause
        
        # Run Father Script manually to get the return code
        from father_agent import run_father_agent as father_check
        approved = father_check()
        
        if approved:
            break
        else:
            with open("feedback.txt", "r", encoding="utf-8") as f:
                feedback_text = f.read()
            run_mother_agent(idea=idea, feedback=feedback_text)
            
    print("\n🚀 Waking up the Orchestrator to start the factory...")
    time.sleep(2)
    subprocess.run([sys.executable, "run_all.py", "--reset"])

if __name__ == "__main__":
    run_parent_loop()