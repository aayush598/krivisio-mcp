from krivisio_tools.github.utils.extract_search_params import extract_search_params_from_text
from krivisio_tools.github.utils.search_repo import search_repo
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Example plain text request from user/document
test_text = """
I need to find repositories related to neural networks in Python.
They should have at least 200 stars and be sorted by stars in descending order.
Show me the top 3 repositories.
"""

# Replace with your GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "your_github_token_here")

# Step 1: Extract search parameters from plain text
params = extract_search_params_from_text(test_text, github_token=GITHUB_TOKEN)
print("Extracted Search Parameters:", params)

# Step 2: Search GitHub repos based on extracted params
repos = search_repo(params)
print("\nTop matching repositories:")
for r in repos:
    print(f"- {r['full_name']} ({r['stars']}⭐) → {r['html_url']}")
