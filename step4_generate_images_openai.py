# ✅ Updated: step4_generate_images_openai.py

import os
import json
import base64
import requests
from pathlib import Path
from datetime import datetime
from config import (
    OPENAI_API_KEY,
    FINAL_PROMPTS,
    OUTPUT_DIR,
    IMAGE_MODEL,
    IMAGE_SIZE,
    IMAGE_QUALITY,
    IMAGE_MODERATION,
    IMAGE_FORMAT,
    IMAGE_BG,
    DEBUG_MODE
)

API_URL = "https://api.openai.com/v1/images/generations"
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

PARAMS_BASE = {
    "model": IMAGE_MODEL,
    "size": IMAGE_SIZE,
    "quality": IMAGE_QUALITY,
    "moderation": IMAGE_MODERATION,
    "output_format": IMAGE_FORMAT,
    "background": IMAGE_BG
}

with open(FINAL_PROMPTS, "r", encoding="utf-8") as f:
    prompts = json.load(f)

OUTPUT_DIR = Path(OUTPUT_DIR)
OUTPUT_DIR.mkdir(exist_ok=True)
Path("debug").mkdir(exist_ok=True)

today_str = datetime.today().strftime("%m%d%Y")

for i, entry in enumerate(prompts):
    prompt = entry["final_prompt"]
    print(f"\n📤 Sending prompt {i+1}/{len(prompts)} to OpenAI...")

    if DEBUG_MODE:
        print("📝 Prompt preview:\n", prompt)

    payload = PARAMS_BASE.copy()
    payload["prompt"] = f"Generate a high-quality image with this prompt: {prompt}"

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        if DEBUG_MODE:
            with open(f"debug/step4_image_response_{i+1}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        if "data" in data and data["data"] and "b64_json" in data["data"][0]:
            b64_data = data["data"][0]["b64_json"]
            image_data = base64.b64decode(b64_data)

            # 🔍 Try to extract character name from the prompt
            try:
                name_part = prompt.split(" from ")[0].strip()
                if name_part.lower().startswith("\""):
                    name_part = name_part[1:]
                char_name = name_part.replace(" ", "_").replace("\"", "").replace(":", "")
            except Exception:
                char_name = f"image_{i+1}"

            filename = f"{char_name}_{today_str}.jpeg"
            output_path = OUTPUT_DIR / filename

            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"💾 Saved to {output_path}")
        else:
            print("⚠️ No image returned or response malformed.")
            if DEBUG_MODE:
                print("🔍 Full response:", json.dumps(data, indent=2))

    except requests.exceptions.HTTPError as err:
        print("❌ HTTP Error:", err)
        if DEBUG_MODE:
            print("🔍 Full response:", response.text)
    except Exception as e:
        print("❌ General error:", e)

print("\n🎉 Step 4 Complete. All available images downloaded.")
