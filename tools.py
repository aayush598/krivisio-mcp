from krivisio_tools.github.main import handle_github_action
from krivisio_tools.side_tools.main import run_tool

from models import GitHubToolInput, GitHubToolOutput

from dotenv import load_dotenv
import os

load_dotenv()

def tool1(input_data: GitHubToolInput) -> GitHubToolOutput:
    return handle_github_action(input_data)


if __name__ == "__main__":
    # Example usage
    input_data = {
        "function": "process_document",
        "data": {
            "document_input": "I need a Python web scraper project with more than 500 stars.",
            "document_type": "text",
            "github_token": os.getenv("GITHUB_TOKEN")
        }
    }
    output = tool1(input_data)
    print(output)