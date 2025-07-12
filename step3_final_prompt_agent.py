import json
import os
import openai
from pathlib import Path
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📁 File paths
STYLE_FILE = "output/style_response.json"
CHAR_FILE = "output/character_response.json"
OUTPUT_FILE = "output/final_prompts.json"

# 📖 Load style and character data
with open(STYLE_FILE, "r", encoding="utf-8") as f:
    style = json.load(f)

with open(CHAR_FILE, "r", encoding="utf-8") as f:
    characters = json.load(f)

# 🧠 Final Prompt Agent instruction
system_prompt = f"""
You are an expert prompt composer for AI image generation. Your role is to take two inputs:

1. A single visual style description:
- Style: {style["style"]}
- Character Placement: {style["character_placement"]}
- Character Size: {style["character_size"]}
- Character Facing: {style["character_facing"]}
- Dimensionality: {style["dimensionality"]}
- Art Profile: {style["art_profile"]}

2. A list of 3 characters:
"""

# Add characters
for c in characters:
    system_prompt += f"""
- Name: {c['name']}
  Origin: {c['origin']}
  Clothing: {c['clothing']}
  Color Scheme: {c['color_scheme']}
"""

system_prompt += """
Generate one cinematic text-to-image prompt for **each character**. Follow these rules:

- Begin each prompt with: [Character] from [Origin] is pictured...
- Describe their appearance and outfit clearly
- Incorporate the style’s setting, lighting, mood, etc.
- Use vivid visual detail (not vague poetry)
- Mention character placement, size, and facing direction
- End each prompt with:
Resolution: 8K
Aspect Ratio: 9:16 (portrait)
Rendering: Ultra-detailed, high dynamic range

Respond in valid JSON format:
[
  { "final_prompt": "..." },
  { "final_prompt": "..." },
  { "final_prompt": "..." }
]
"""

# 💬 Call ChatGPT
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": system_prompt}],
    temperature=0.8
)

# 📦 Get content and clean markdown-style code blocks
content = response.choices[0].message.content.strip()

# 🧪 Debug output
print("\n🧪 GPT RAW OUTPUT:\n")
print(content)

# 🧼 Remove ```json or ``` wrappers
if content.startswith("```json"):
    content = content.removeprefix("```json").removesuffix("```").strip()
elif content.startswith("```"):
    content = content.removeprefix("```").removesuffix("```").strip()

# 🧾 Try parsing JSON
try:
    prompts = json.loads(content)
except json.JSONDecodeError as e:
    print("\n❌ JSON Decode Error:", e)
    print("GPT likely returned text instead of JSON. Fix prompt or log the output above.")
    exit(1)


# 💾 Save parsed prompts
Path("output").mkdir(exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(prompts, f, indent=2)

print("\n✅ Step 3 Complete. Final prompts saved to:", OUTPUT_FILE)
