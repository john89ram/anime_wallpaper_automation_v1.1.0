
import json
import openai
from pathlib import Path
from config import OPENAI_API_KEY, STYLE_RESPONSE, CHARACTER_RESPONSE, FINAL_PROMPTS, OPENAI_MODEL, DEFAULT_ASPECT_RATIO, DEFAULT_RESOLUTION, DEFAULT_RENDERING

openai.api_key = OPENAI_API_KEY

with open(STYLE_RESPONSE, "r", encoding="utf-8") as f:
    style = json.load(f)
with open(CHARACTER_RESPONSE, "r", encoding="utf-8") as f:
    characters = json.load(f)

system_prompt = f"""
You are an expert prompt composer for AI image generation. Your role is to take two inputs:

1. A single visual style description:
- Style: {style["style"]}
- Character Placement: {style["character_placement"]}
- Character Size: {style["character_size"]}
- Character Facing: {style["character_facing"]}
- Dimensionality: {style["dimensionality"]}
- Art Profile: {style["art_profile"]}

2. A list of characters:
"""

for c in characters:
    system_prompt += f"""
- Name: {c['name']}
  Origin: {c['origin']}
  Clothing: {c['clothing']}
  Color Scheme: {c['color_scheme']}
"""

system_prompt += f"""
Generate one cinematic text-to-image prompt for **each character**. Follow these rules:

- Begin each prompt with: [Character] from [Origin] is pictured...
- Describe their appearance and outfit clearly
- Incorporate the style’s setting, lighting, mood, etc.
- Use vivid visual detail (not vague poetry)
- Mention character placement, size, and facing direction
- End each prompt with:
Resolution: {DEFAULT_RESOLUTION}
Aspect Ratio: {DEFAULT_ASPECT_RATIO}
Rendering: {DEFAULT_RENDERING}

Respond in valid JSON format:
[
  {{ "final_prompt": "..." }},
  {{ "final_prompt": "..." }},
  {{ "final_prompt": "..." }}
]
"""

response = openai.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[{"role": "system", "content": system_prompt}],
    temperature=0.8
)

content = response.choices[0].message.content.strip()
if content.startswith("```json"):
    content = content.removeprefix("```json").removesuffix("```").strip()
elif content.startswith("```"):
    content = content.removeprefix("```").removesuffix("```").strip()

try:
    prompts = json.loads(content)
except json.JSONDecodeError as e:
    print("\n❌ JSON Decode Error:", e)
    print("GPT likely returned text instead of JSON. Fix prompt or log the output above.")
    exit(1)

Path(FINAL_PROMPTS).parent.mkdir(exist_ok=True)
with open(FINAL_PROMPTS, "w", encoding="utf-8") as f:
    json.dump(prompts, f, indent=2)

print("\n✅ Step 3 Complete. Final prompts saved to:", FINAL_PROMPTS)