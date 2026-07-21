from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

print("🔍 Fetching available models for your API key...")

try:
    # Just print the raw name of every model available
    for model in client.models.list():
        print(f"✅ {model.name}")
except Exception as e:
    print(f"❌ Error fetching models: {e}")