## [1.3.0] - 2025-07-13

### 🎨 Character Preservation & Prompt Refinement
- Characters now stay true to original style — no forced cyberpunk armor.
- Step 2 rewired to enhance, not override.
  
### 📝 Final Prompt Logging
- Final prompts saved as `FirstName_MMDDYYYY.txt` for traceability.

### 📁 Output Directory Restructure
- `output/json` for debug + GPT outputs
- `output/logs/images` for generated wallpapers
- `output/logs/final_prompt_history` for individual prompt archives

---

## [1.1.0] - 2025-07-12
Version: 1.1.0
Release Date: 2025-07-12

CHANGELOG:

🔄 Directory Versioning
- Project renamed to anime_wallpaper_automation_v1.1.0 to reflect structural improvements.

✅ .gitignore Cleanup
- Added a comprehensive .gitignore to exclude:
  - .env
  - venv/
  - output/
  - __pycache__/
  - node_modules/
  - image files, log files, and system junk

🔐 Environment File Protection
- Confirmed .env is no longer tracked by Git.
- Added .env and **/.env to .gitignore and verified .env is untracked via git ls-files.

⚙️ Configuration Refactor (Prep)
- Defined shared values and constants across the project for future cleanup.
- Created config.py template (planned) to centralize:
  - OpenAI key and model
  - Input/output paths
  - Image generation parameters
  - Prompt formatting settings

🧹 Output Cleanup
- Deleted stale files in output/:
  - Auto-generated images (image-1.jpeg/png, etc.)
  - Outdated JSON prompt files (styles.json, characters.json, exclusions.json)

💡 Git Usage Updates
- Set upstream tracking for GitHub repo via git push --set-upstream origin main.
- Removed unused tracked files using git rm --cached.
- Verified .env stays local and untracked.

🚀 Ready for next version:
- Full config.py integration across all steps
- Optional CLI/GUI toggle
- Style/character test set toggle