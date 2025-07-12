import json
import os
import random
import openai
from pathlib import Path
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📁 File paths
CHAR_FILE = "characters.json"
EXCLUDE_FILE = "exclusions.json"
OUTPUT_FILE = "output/character_response.json"

# 📖 Load character list
with open(CHAR_FILE, "r", encoding="utf-8") as f:
    characters = json.load(f)

# ❌ Filter exclusions if provided
if Path(EXCLUDE_FILE).exists():
    with open(EXCLUDE_FILE, "r", encoding="utf-8") as f:
        exclusions = set(json.loads(f.read().strip()))
    characters = [c for c in characters if c["name"] not in exclusions]

# 🎲 Randomly select 3 characters
selected = random.sample(characters, 3)

# 🧠 Build system prompt for Character Agent
character_prompt = f"""
You are an expert character selector and descriptor for AI image generation. Your task is to return the following characters using this structure:

[
  {{
    "name": "{selected[0]['name']}",
    "origin": "{selected[0]['origin']}",
    "clothing": "{selected[0]['clothing']}",
    "color_scheme": "{selected[0]['color_scheme']}"
  }},
  {{
    "name": "{selected[1]['name']}",
    "origin": "{selected[1]['origin']}",
    "clothing": "{selected[1]['clothing']}",
    "color_scheme": "{selected[1]['color_scheme']}"
  }},
  {{
    "name": "{selected[2]['name']}",
    "origin": "{selected[2]['origin']}",
    "clothing": "{selected[2]['clothing']}",
    "color_scheme": "{selected[2]['color_scheme']}"
  }}
]
"""

# 💬 Call ChatGPT to finalize formatting (or skip this if you trust your data)
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": character_prompt}],
    temperature=0.7
)

# 🧾 Parse and Save
result = response.choices[0].message.content
char_json = json.loads(result)

Path("output").mkdir(exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(char_json, f, indent=2)

print("✅ Step 2 Complete. Character data saved to:", OUTPUT_FILE)
print(f"\n🎴 Selected characters: {[c['name'] for c in selected]}")
