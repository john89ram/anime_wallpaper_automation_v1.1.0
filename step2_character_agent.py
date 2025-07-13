# ✅ Updated: step2_character_agent.py

import json
import os
import random
import re
from openai import OpenAI
from config import (
    OPENAI_API_KEY,
    CHARACTER_FILE,
    CHARACTER_RESPONSE,
    NUM_CHARACTERS,
    USE_TEST_INPUT,
    DEBUG_MODE
)

if DEBUG_MODE:
    print(f"🧪 Using test input: {USE_TEST_INPUT}")

client = OpenAI(api_key=OPENAI_API_KEY)

# 📁 Load character list
with open(CHARACTER_FILE, "r", encoding="utf-8") as f:
    character_list = json.load(f)

selected = random.sample(character_list, NUM_CHARACTERS)
character_summary = "\n".join([f"{c['name']} from {c['origin']}" for c in selected])

if DEBUG_MODE:
    print("🎯 Selected characters:")
    for c in selected:
        print(f" - {c['name']} from {c['origin']}")

user_prompt = f"""
Take the following {NUM_CHARACTERS} anime characters and adapt their outfits slightly to match a more cinematic wallpaper style — without losing their original identity.
Do NOT change who they are. Keep iconic outfits recognizable, just enhance or refine them slightly to reflect the mood and colors of a wallpaper setting.
Return only a JSON array with:
- name
- origin
- clothing
- color_scheme (wallpaper-appropriate)

Characters:
{character_summary}
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a character styling assistant."},
        {"role": "user", "content": user_prompt.strip()}
    ],
    temperature=0.7,
    max_tokens=500
)

result = response.choices[0].message.content.strip()
clean_json = re.sub(r"^```(json)?|```$", "", result.strip(), flags=re.MULTILINE).strip()

if DEBUG_MODE:
    print("🔎 Raw GPT output:\n", result)
    os.makedirs("debug", exist_ok=True)
    with open("debug/step2_characters_raw.json", "w", encoding="utf-8") as f:
        f.write(result)

try:
    char_json = json.loads(clean_json)
except json.JSONDecodeError as e:
    print("❌ Failed to decode JSON. Output:\n", clean_json)
    print(f"\n❗ JSONDecodeError: {e}")
    exit(1)

os.makedirs(os.path.dirname(CHARACTER_RESPONSE), exist_ok=True)
with open(CHARACTER_RESPONSE, "w", encoding="utf-8") as f:
    json.dump(char_json, f, indent=2, ensure_ascii=False)

print(f"✅ Saved re-styled characters to {CHARACTER_RESPONSE}:")
for i, char in enumerate(char_json, 1):
    print(f"{i}. {char['name']} from {char['origin']}")
    print(f"   - Clothing: {char['clothing']}")
    print(f"   - Color Scheme: {char['color_scheme']}\n")
