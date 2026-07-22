import os
import time
from google import genai

# Make sure you have your GEMINI_API_KEY set in your .env file
# pip install google-genai

print("===================================================")
print("☁️ BOOTING GOOGLE ANTIGRAVITY MANAGED AGENT")
print("===================================================")

def delegate_to_antigravity(task_description: str):
    """
    Replaces the local Docker and Ollama loop by delegating the task 
    to Google's managed Antigravity Linux sandbox.
    """
    try:
        client = genai.Client()
        
        # We append our strict agency rules to the user's prompt
        agency_rules = """
        You are acting on behalf of an elite AI Software Agency. 
        Before you finish, you must:
        1. Write the code.
        2. Write a unit test.
        3. Run the test in your sandbox.
        4. Scan the code for security vulnerabilities.
        """
        
        full_prompt = f"{agency_rules}\n\nTask: {task_description}"
        
        print(f"🚀 Dispatching task to antigravity-preview-05-2026...")
        print("⏳ The agent is now planning, executing, and testing in the cloud...")
        
        # The Antigravity agent runs an autonomous loop (plan, act, observe) 
        # inside a secure remote Linux environment with filesystem and tool access.
        interaction = client.create(
            agent="antigravity-preview-05-2026",
            input=full_prompt,
            environment="remote", 
        )
        
        print("\n✅ [Antigravity Agent] Task Complete. Artifacts & Output:")
        print("---------------------------------------------------")
        print(interaction.output_text)
        print("---------------------------------------------------")
        
    except Exception as e:
        print(f"❌ Failed to communicate with Google Antigravity: {e}")

if __name__ == "__main__":
    sample_task = "Create a Next.js dashboard component for lead tracking, write a Jest test for it, and verify it compiles."
    delegate_to_antigravity(sample_task)