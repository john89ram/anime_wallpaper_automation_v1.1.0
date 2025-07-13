import os
import json
import re
import random
from openai import OpenAI

# 🔑 Init API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📁 Load characters.json
characters_path = os.path.join("input", "characters.json")
with open(characters_path, "r", encoding="utf-8") as f:
    character_list = json.load(f)

# 🎲 Pick 3 random characters
selected = random.sample(character_list, 3)

# ✏️ Build content for GPT
character_summary = "\n".join([
    f"{char['name']} from {char['origin']}" for char in selected
])

user_prompt = f"""
Take the following 3 anime characters and redesign them for a **dramatic cyberpunk anime scene**.

Keep their names and origins the same, but reimagine their clothing and color_scheme to match a cyberpunk theme. 
Output only a JSON array where each object contains:
- name
- origin
- clothing (reimagined)
- color_scheme (reimagined)

Characters:
{character_summary}
"""

# 🌐 GPT call
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a character styling assistant."},
        {"role": "user", "content": user_prompt.strip()}
    ],
    temperature=0.7,
    max_tokens=500
)

# 📤 Extract and clean the response
result = response.choices[0].message.content.strip()
clean_json = re.sub(r"^```(json)?|```$", "", result.strip(), flags=re.MULTILINE).strip()

# 🧪 Decode JSON
try:
    char_json = json.loads(clean_json)
except json.JSONDecodeError as e:
    print("❌ Failed to decode JSON. Output:\n", clean_json)
    print(f"\n❗ JSONDecodeError: {e}")
    exit(1)

# 💾 Save to ./output/character_response.json
output_dir = os.path.join(os.getcwd(), "output")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "character_response.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(char_json, f, indent=2, ensure_ascii=False)

# ✅ Done
print(f"✅ Saved re-styled characters to {output_path}:\n")
for i, char in enumerate(char_json, 1):
    print(f"{i}. {char['name']} from {char['origin']}")
    print(f"   - Clothing: {char['clothing']}")
    print(f"   - Color Scheme: {char['color_scheme']}\n")
