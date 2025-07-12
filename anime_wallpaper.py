import os
import subprocess
from pathlib import Path

# 📁 Check required files
required_files = [
    "styles.json",
    "characters.json",
    ".env"
]

missing = [f for f in required_files if not Path(f).exists()]
if missing:
    print("❌ Missing required files:", ", ".join(missing))
    exit(1)

# 📁 Create output folder if needed
Path("output").mkdir(exist_ok=True)

# 🧪 Run each step
steps = [
    ("Step 1 - Style Agent", "step1_style_agent.py"),
    ("Step 2 - Character Agent", "step2_character_agent.py"),
    ("Step 3 - Final Prompt Agent", "step3_final_prompt_agent.py"),
    ("Step 4 - Image Generator", "step4_generate_images_openai.py")
]

for label, script in steps:
    print(f"\n🚀 {label} running: {script}")
    result = subprocess.run(["python", script])
    if result.returncode != 0:
        print(f"\n❌ {label} failed. Stopping automation.")
        exit(result.returncode)

print("\n✅ All steps completed successfully!")
