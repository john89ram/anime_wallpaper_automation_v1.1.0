# ✅ Updated: step1_style_agent.py

import json
import random
import openai
from pathlib import Path
from config import (
    OPENAI_API_KEY,
    STYLE_FILE,
    STYLE_RESPONSE,
    DEFAULT_TARGET,
    OPENAI_MODEL,
    USE_TEST_INPUT,
    DEBUG_MODE
)

if DEBUG_MODE:
    print(f"\U0001f9ea Using test input: {USE_TEST_INPUT}")

# 🔐 Set API key
openai.api_key = OPENAI_API_KEY

# 📖 Load styles
with open(STYLE_FILE, "r", encoding="utf-8") as f:
    style_pool = json.load(f)

# 🎲 Pick a style
selected_style = random.choice(style_pool)

if DEBUG_MODE:
    print(f"🎯 Selected style: {selected_style}")

# 🧠 Build system prompt
style_agent_prompt = f"""
You are an expert visual style generator for AI image creation. Your job is to create visual prompts for live AI wallpapers that showcase {DEFAULT_TARGET}. You do **not** describe the character directly. Your focus is to define the artistic and visual direction of the image.

Your selected style is:
**{selected_style}**

For visual consistency and to avoid disproportionate body rendering, always assume:
- Full-body framing with balanced anatomy
- Equal attention to both upper and lower body
- Phrases like "athletically proportioned," "standing tall," or "natural leg length" where appropriate
- Avoid short or exaggerated torso-heavy perspectives

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
result = response.choices[0].message.content.strip()

if DEBUG_MODE:
    print("\U0001f50e Raw GPT output:\n", result)
    Path("debug").mkdir(exist_ok=True)
    with open("debug/step1_style_raw.json", "w", encoding="utf-8") as f:
        f.write(result)

style_json = json.loads(result)

Path(STYLE_RESPONSE).parent.mkdir(exist_ok=True)
with open(STYLE_RESPONSE, "w", encoding="utf-8") as f:
    json.dump(style_json, f, indent=2)

print("✅ Step 1 Complete. Style saved to:", STYLE_RESPONSE)
