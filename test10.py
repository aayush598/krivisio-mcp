from krivisio_tools.github.utils.suggestions_techstack_features import process_document
from dotenv import load_dotenv
import os
import json
import time

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    start_time = time.time()  # Record the start time

    result = process_document(
        input_source="I need a Python web scraper project with more than 500 stars.",
        source_type="text",
        github_token=os.getenv("GITHUB_TOKEN", "your_github_token_here")
    )
    
    end_time = time.time()  # Record the end time
    processing_time = end_time - start_time  # Calculate the duration

    print(f"Document processed in {processing_time:.4f} seconds.")
    print(json.dumps(result, indent=2))