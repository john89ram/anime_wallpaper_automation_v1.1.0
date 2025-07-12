import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import requests

# 🔐 Load API key from .env (optional)
load_dotenv()
CUSTOM_API_KEY = os.getenv("CUSTOM_IMAGE_API_KEY")  # or hardcode below

# 🌐 Your custom image generation API endpoint
CUSTOM_API_URL = "https://your.image.api/generate"

# 📁 Files
PROMPT_FILE = "output/final_prompts.json"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# 📖 Load prompts
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    prompts = json.load(f)

# 🎨 Image generation loop
for idx, prompt in enumerate(prompts):
    prompt_text = prompt["final_prompt"]
    print(f"\n📤 Sending prompt {idx + 1}/{len(prompts)} to custom image API...")
    print("📝 Prompt preview:\n", prompt_text)

    payload = {
        "model": "gpt-image-1",
        "prompt": f"Generate a high-quality image with this prompt: {prompt_text}",
        "size": "1024x1536",
        "quality": "high",
        "moderation": "low",
        "output_format": "jpeg",
        "background": "opaque",
        "output_compression": 50
    }

    headers = {
        "Authorization": f"Bearer {CUSTOM_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(CUSTOM_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()

        # Get image URL or base64 (depending on API)
        if "image_url" in response_json:
            image_url = response_json["image_url"]
            print("✅ Image URL received. Downloading...")

            img_data = requests.get(image_url).content
            out_file = OUTPUT_DIR / f"image-{idx + 1}.jpg"
            with open(out_file, "wb") as f:
                f.write(img_data)
            print(f"💾 Saved to {out_file}")

        elif "image_base64" in response_json:
            import base64
            image_data = base64.b64decode(response_json["image_base64"])
            out_file = OUTPUT_DIR / f"image-{idx + 1}.jpg"
            with open(out_file, "wb") as f:
                f.write(image_data)
            print(f"💾 Saved to {out_file}")

        else:
            print("⚠️ Unexpected response format:", response_json)

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        print("❗ Payload was:\n", json.dumps(payload, indent=2))
        continue

    # ⏱️ Wait between calls (adjust if needed)
    time.sleep(1.5)

print("\n🎉 Step 4 Complete. All available images downloaded.")
