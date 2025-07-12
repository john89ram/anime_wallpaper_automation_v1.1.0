import os
import requests
import json
from dotenv import load_dotenv

# Load your OpenAI API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Endpoint and headers
url = "https://api.openai.com/v1/images/generations"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Clean, valid payload
payload = {
    "model": "gpt-image-1",
    "prompt": "Generate a high-quality image of a samurai under the cherry blossoms.",
    "size": "1024x1024",           # or "1024x1536", "1536x1024"
    "quality": "high",             # or "standard"
    "moderation": "low",           # Optional; reduce false flags
    "output_format": "jpeg",       # jpeg, png
    "background": "opaque",        # opaque, transparent (for PNG only)
    # "output_compression": 50     # Only supported for PNGs (remove for JPEGs)
}

# Send POST request
response = requests.post(url, headers=headers, json=payload)

# Show the response
try:
    response.raise_for_status()
    print("\n✅ Success! Full response:\n")
    print(json.dumps(response.json(), indent=2))
except requests.exceptions.HTTPError as e:
    print("❌ HTTP error:", e)
    print("🔍 Full response:", response.text)
