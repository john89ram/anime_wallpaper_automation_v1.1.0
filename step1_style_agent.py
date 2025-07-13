
import json
import random
import openai
from pathlib import Path
from config import OPENAI_API_KEY, STYLE_FILE, STYLE_RESPONSE, DEFAULT_TARGET, OPENAI_MODEL
from config import USE_TEST_INPUT
print(f"🧪 Using test input: {USE_TEST_INPUT}")

# 🔐 Set API key
openai.api_key = OPENAI_API_KEY

# 📖 Load styles
with open(STYLE_FILE, "r", encoding="utf-8") as f:
    style_pool = json.load(f)

# 🎲 Pick a style
selected_style = random.choice(style_pool)

# 🧠 Build system prompt
style_agent_prompt = f"""
You are an expert visual style generator for AI image creation. Your job is to create visual prompts for live AI wallpapers that showcase {DEFAULT_TARGET}. You do **not** describe the character directly. Your focus is to define the artistic and visual direction of the image.

Your selected style is:
**{selected_style}**

Output one result in this format (valid JSON):
{{
  "title": "",
  "caption": "",
  "style": "",
  "character_placement": "",
  "character_size": "",
  "character_facing": "",
  "dimensionality": "",
  "art_profile": ""
}}
"""

# 💬 Call ChatGPT
response = openai.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[{"role": "system", "content": style_agent_prompt}],
    temperature=0.9
)

# 🧾 Parse & Save
result = response.choices[0].message.content
style_json = json.loads(result)

Path(STYLE_RESPONSE).parent.mkdir(exist_ok=True)
with open(STYLE_RESPONSE, "w", encoding="utf-8") as f:
    json.dump(style_json, f, indent=2)

print("✅ Step 1 Complete. Style saved to:", STYLE_RESPONSE)
