from krivisio_tools.github.utils.search_repo import search_repo
from dotenv import load_dotenv
import os   

# Load environment variables from .env file
load_dotenv()

# Example usage of the search_repo function
# Ensure you have set the GITHUB_TOKEN in your .env file or environment variables
# You can adjust the parameters as needed for your search criteria

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

input_data = {
    "token": GITHUB_TOKEN,
    "query": "machine learning",
    "limit": 3,
    "category": "Python",
    "stars": ">=100",
    "sort": "stars",
    "order": "desc"
}

repos = search_repo(input_data)
for r in repos:
    print(f"Repository: {r['name']}, Stars: {r['stars']}, URL: {r['html_url']}")
    # print(r)
