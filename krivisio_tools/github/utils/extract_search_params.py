# krivisio_tools/github/utils/extract_search_params.py

from typing import Dict, Any
from krivisio_tools.github.utils.llm_client import chat_with_llm
import json

def extract_search_params_from_text(
    extracted_text: str,
    github_token: str
) -> Dict[str, Any]:
    """
    Uses the LLM to parse extracted text and return search_repo parameters.

    Args:
        extracted_text (str): Raw text from a document or user input.
        github_token (str): GitHub token to include in the result.

    Returns:
        dict: Parameters ready for search_repo.
    """
    prompt = f"""
    You are a system that extracts search parameters for finding GitHub repositories.
    The extracted text will contain details about the type of project a user wants.
    Your output must be a valid JSON dictionary with only these keys:
    - query (string, required) — search keywords
    - limit (integer, optional) — number of repositories to return
    - category (string, optional) — programming language or topic
    - stars (string, optional) — star filter, e.g. '>100' or '>=500'
    - sort (string, optional) — 'stars', 'forks', or 'updated'
    - order (string, optional) — 'asc' or 'desc'

    Rules:
    - If a field is not explicitly mentioned, omit it from the JSON.
    - Ensure output is strictly JSON with no explanations.

    Extract parameters from the following text:
    ---
    {extracted_text}
    ---
    """

    raw_response = chat_with_llm(prompt)
    
    try:
        params = json.loads(raw_response)  # We can replace eval with json.loads if we trust JSON format
        if not isinstance(params, dict):
            raise ValueError("LLM output is not a dictionary.")
    except Exception as e:
        raise ValueError(f"Failed to parse LLM output: {e}\nOutput was: {raw_response}")

    # Always add token
    params["token"] = github_token

    return params
