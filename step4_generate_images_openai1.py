import os
import json
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# 📁 Config
PROMPT_FILE = "output/final_prompts.json"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# 🖼 Image generation config
API_URL = "https://api.openai.com/v1/images/generations"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
PARAMS_BASE = {
    "model": "gpt-image-1",
    "size": "1024x1536",
    "quality": "high",
    "moderation": "low",
    "output_format": "jpeg",
    "background": "opaque"
    # ❌ Do NOT include 'response_format'
}

# 📖 Load prompts
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    prompts = json.load(f)

# 📤 Generate and save each image
for i, entry in enumerate(prompts):
    prompt = entry["final_prompt"]
    print(f"\n📤 Sending prompt {i+1}/{len(prompts)} to OpenAI...")
    print("📝 Prompt preview:\n", prompt[:300], "...")

    payload = PARAMS_BASE.copy()
    payload["prompt"] = f"Generate a high-quality image with this prompt: {prompt}"

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        if "data" in data and data["data"] and "b64_json" in data["data"][0]:
            b64_data = data["data"][0]["b64_json"]
            image_data = base64.b64decode(b64_data)
            output_path = OUTPUT_DIR / f"image-{i+1}.jpeg"

            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"💾 Saved to {output_path}")
        else:
            print("⚠️ No image returned or response malformed.")
            print("🔍 Full response:", json.dumps(data, indent=2))

    except requests.exceptions.HTTPError as err:
        print("❌ HTTP Error:", err)
        print("🔍 Full response:", response.text)
    except Exception as e:
        print("❌ General error:", e)

print("\n🎉 Step 4 Complete. All available images downloaded.")
