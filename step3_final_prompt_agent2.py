import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import openai

# 🔐 Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📁 File paths
STYLE_FILE = "output/style_response.json"
CHARACTER_FILE = "output/character_response.json"
OUTPUT_FILE = "output/final_prompts.json"

# 📖 Load style and characters
with open(STYLE_FILE, "r", encoding="utf-8") as f:
    style = json.load(f)

with open(CHARACTER_FILE, "r", encoding="utf-8") as f:
    characters = json.load(f)

# 🧠 System prompt (instructions to GPT)
system_prompt = """
You are a prompt fusion agent that combines visual style and character info into cinematic AI image prompts.

Rules:
1. Use the provided 'character' and 'style' objects.
2. Begin each prompt with: Anime illustration of [name] from [origin], wearing [clothing].
3. Include the character placement, size, facing direction, dimensionality, and art profile.
4. Include the character's color scheme to help guide styling.
5. Wrap your response as: { "final_prompt": "..." }
6. Append rendering specs exactly:
Resolution: 8K Aspect Ratio: 9:16 (portrait) Rendering: Ultra-detailed, high dynamic range.
Only return valid JSON. Do not explain anything. Return one object per response.
"""

# 🔁 Generate one prompt per character
all_prompts = []

for idx, char in enumerate(characters):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps({
            "character": char,
            "style": style
        }, indent=2)}
    ]

    print(f"\n📤 Sending character {idx+1}/{len(characters)}: {char['name']}")

    # 🧠 GPT call
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7
    )

    raw_output = response.choices[0].message.content.strip()
    print(f"🧪 Raw output for {char['name']}:\n{raw_output}\n")

    # 🧼 Clean markdown/code wrappers
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_output.strip(), flags=re.IGNORECASE)

    try:
        prompt = json.loads(cleaned)
        all_prompts.append(prompt)
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON Decode Error for {char['name']}: {e}")
        print("⚠️ Raw cleaned content:\n", cleaned)
        continue

# 💾 Save to file
Path("output").mkdir(exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_prompts, f, indent=2)

print(f"\n✅ Step 3 Complete. Final prompts saved to: {OUTPUT_FILE}")
