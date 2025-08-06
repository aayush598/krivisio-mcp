# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# You can add more config variables if needed
DEFAULT_MODEL = "gpt-4o"  # or "gpt-3.5-turbo", etc.
TEMPERATURE = 0.1
MAX_TOKENS = 2000

MANAGER_SCORE_THRESHOLD = 4.0  # Minimum score for manager candidates
AVG_TEAM_SIZE = 3.0  # Average team size for selection