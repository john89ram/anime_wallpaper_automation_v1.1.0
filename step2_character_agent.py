
import json
import os
import random
import re
from openai import OpenAI
from config import OPENAI_API_KEY, CHARACTER_FILE, CHARACTER_RESPONSE, NUM_CHARACTERS
from config import USE_TEST_INPUT
print(f"🧪 Using test input: {USE_TEST_INPUT}")

client = OpenAI(api_key=OPENAI_API_KEY)

# 📁 Load character list
with open(CHARACTER_FILE, "r", encoding="utf-8") as f:
    character_list = json.load(f)

selected = random.sample(character_list, NUM_CHARACTERS)
character_summary = "\n".join([f"{c['name']} from {c['origin']}" for c in selected])

user_prompt = f"""
Take the following {NUM_CHARACTERS} anime characters and redesign them for a **dramatic cyberpunk anime scene**.
Keep their names and origins the same, but reimagine their clothing and color_scheme to match a cyberpunk theme. 
Output only a JSON array where each object contains:
- name
- origin
- clothing (reimagined)
- color_scheme (reimagined)

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