from krivisio_tools.github.utils.extract_repo_features import extract_features_and_stack
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "your_github_token_here")

repos = [
    "https://github.com/pytorch/pytorch",
    "https://github.com/pyg-team/pytorch_geometric"
]

results = extract_features_and_stack(GITHUB_TOKEN, repos)

print("Extracted Features and Tech Stack:")
if not results:
    print("No repositories found or no README content available.")
else:  
    print(f"Results : {results}")
