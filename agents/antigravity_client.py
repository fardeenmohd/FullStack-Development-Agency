import os
import re
from google import genai
from env_setup import get_gemini_key

def delegate_to_cloud(task_description, target_file, existing_code=""):
    """
    Sends the task to the Google Antigravity Cloud Sandbox.
    Instead of just returning text, the cloud agent loops, writes, and tests the code remotely.
    """
    print(f"☁️ [Cloud SDK] Uplinking to Google Servers for: {target_file}...")
    
    # Initialize the official Google GenAI Client
    client = genai.Client(api_key=get_gemini_key())
    
    # We use the managed agentic model with remote code execution capabilities
    model_id = "gemini-2.5-pro" # Note: In production, swap to antigravity-preview-05-2026 if enabled
    
    prompt = f"""
    You are the Lead Dispatcher. Your task is to write or update the following file: {target_file}
    
    TICKET DESCRIPTION:
    {task_description}
    
    EXISTING CODE:
    {existing_code if existing_code else "File is currently empty."}
    
    You MUST respond with the complete, fully functioning code for this file.
    Format your response EXACTLY like this:
    
    CONTENT:
    <the raw code goes here>
    END_CONTENT
    """

    try:
        # We enable code execution so the AI can test its own logic in Google's sandbox
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.2,
                tools=[{"code_execution": {}}] 
            )
        )
        
        # Extract the code block from the cloud agent's response
        match = re.search(r"CONTENT:\n(.*?)\nEND_CONTENT", response.text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            # Fallback if the AI just returns raw code without the wrapper
            return response.text.replace("```python", "").replace("```typescript", "").replace("```", "").strip()
            
    except Exception as e:
        print(f"❌ [Cloud SDK] Uplink failed: {e}")
        return None