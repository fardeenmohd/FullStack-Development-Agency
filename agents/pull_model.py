import requests
import json

OLLAMA_URL = "http://localhost:11434/api/pull"
MODEL_NAME = "qwen2.5-coder:7b"

print(f"📥 Forcing Ollama server to download '{MODEL_NAME}' via API...")
print("This is a ~4GB download. Please wait (this may take 5-10 minutes).")
print("Do not close this window until it says 'Done!'...")

try:
    response = requests.post(OLLAMA_URL, json={"name": MODEL_NAME}, stream=True)
    response.raise_for_status()

    for line in response.iter_lines():
        if line:
            body = json.loads(line)
            status = body.get("status", "")
            # If it provides download details, print them nicely
            if "completed" in body and "total" in body:
                percent = (body["completed"] / body["total"]) * 100
                print(f"\rDownloading... {percent:.1f}%", end="")
            elif status:
                print(f"\nStatus: {status}")

    print("\n\n✅ Done! The model is successfully downloaded and ready for the 3070 Ti.")

except requests.exceptions.ConnectionError:
    print("❌ Error: Could not connect to Ollama. Make sure the Ollama app is running in your Windows tray!")
except Exception as e:
    print(f"\n❌ Error pulling model: {e}")