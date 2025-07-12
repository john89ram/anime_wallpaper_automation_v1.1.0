import json
import os
import openai
import requests
from pathlib import Path
from dotenv import load_dotenv

# 🔐 Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📁 Paths
PROMPT_FILE = "output/final_prompts.json"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# 📖 Load prompts
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    prompts = json.load(f)

# 🎨 Generate and save images
for i, item in enumerate(prompts):
    prompt = item["final_prompt"]
    print(f"\n📤 Sending prompt {i+1}/3 to OpenAI...")

    response = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1536",  # Portrait 9:16
        quality="high",
        moderation="low",
        output_format="jpeg",
        background="opaque",
        output_compression=50,
    )

    image_url = response.data[0].url
    print(f"✅ Image {i+1} generated. Downloading...")

    image_data = requests.get(image_url).content
    file_path = OUTPUT_DIR / f"image-{i+1}.png"
    with open(file_path, "wb") as f:
        f.write(image_data)

    print(f"💾 Saved to {file_path}")

print("\n🎉 Step 4 Complete. All images generated and saved!")
