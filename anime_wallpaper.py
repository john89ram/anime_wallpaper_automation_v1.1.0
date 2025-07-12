import subprocess
import sys
import os
from pathlib import Path

def run_step(step_number, script_name):
    print(f"\n🚀 Step {step_number} - Running: {script_name}")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"✅ Step {step_number} - {script_name} complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Step {step_number} - {script_name} failed. Stopping automation.")
        sys.exit(1)

def main():
    print("🎨 Anime Wallpaper Automation Started!")

    # Optional: create output folder
    Path("output").mkdir(exist_ok=True)

    # Step 1 - Style Agent
    run_step(1, "step1_style_agent.py")

    # Step 2 - Character Agent
    run_step(2, "step2_character_agent.py")

    # Step 3 - Final Prompt Agent
    run_step(3, "step3_final_prompt_agent.py")

    # Step 4 - Generate Images (OpenAI or Custom API)
    run_step(4, "step4_generate_images_openai.py")
    # Or swap if you're using a custom API
    # run_step(4, "step4_generate_images_custom.py")

    print("\n🎉 All steps complete! Your wallpapers are ready in the output/ folder.")

if __name__ == "__main__":
    main()
