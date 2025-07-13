import os
from dotenv import load_dotenv

# 🔐 Load environment
load_dotenv()

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Toggle for test input mode ===
USE_TEST_INPUT = False  # Set to False in production

# === File Paths ===
INPUT_DIR = "input"
OUTPUT_DIR = "output"

STYLE_FILE = f"{INPUT_DIR}/{'styles_test.json' if USE_TEST_INPUT else 'styles.json'}"
CHARACTER_FILE = f"{INPUT_DIR}/{'characters_test.json' if USE_TEST_INPUT else 'characters.json'}"

STYLE_RESPONSE = f"{OUTPUT_DIR}/style_response.json"
CHARACTER_RESPONSE = f"{OUTPUT_DIR}/character_response.json"
FINAL_PROMPTS = f"{OUTPUT_DIR}/final_prompts.json"

# === OpenAI Settings ===
OPENAI_MODEL = "gpt-4o"
IMAGE_MODEL = "gpt-image-1"
IMAGE_SIZE = "1024x1536"
IMAGE_QUALITY = "high"
IMAGE_MODERATION = "low"
IMAGE_FORMAT = "jpeg"
IMAGE_BG = "opaque"

# === App Settings ===
NUM_CHARACTERS = 3
DEFAULT_TARGET = "anime characters"
DEFAULT_ASPECT_RATIO = "9:16 (portrait)"
DEFAULT_RESOLUTION = "8K"
DEFAULT_RENDERING = "Ultra-detailed, high dynamic range"
