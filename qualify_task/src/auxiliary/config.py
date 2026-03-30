import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONSIDER_SRC_FILES = os.getenv("CONSIDER_SRC_FILES", 0)
DEFAULT_LLM_MODEL = "gpt-4o-mini"

PROMPTS_FOLDER = "src/prompts/"
CONSIDER_SRC_PROMPT = "consider_src.txt"
IGNORE_SRC_PROMPT = "ignore_src.txt"
