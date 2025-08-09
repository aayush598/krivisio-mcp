from krivisio_tools.github.utils.suggestions_techstack_features import process_document
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    result = process_document(
        input_source="I need a Python web scraper project with more than 500 stars.",
        source_type="text",
        github_token=os.getenv("GITHUB_TOKEN", "your_github_token_here"
    )
    )
    import json
    print(json.dumps(result, indent=2))
