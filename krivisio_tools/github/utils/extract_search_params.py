from typing import Dict, Any
from krivisio_tools.github.utils.llm_client import chat_with_llm
import json

def extract_search_params_from_text(
    extracted_text: str,
    github_token: str
) -> Dict[str, Any]:
    """
    Extracts only the search query and programming language category from text.
    All other parameters are static defaults.
    """

    prompt = f"""
    You are a system that extracts ONLY:
    - query (string) — the search keywords
    - category (string) — the programming language or topic

    The extracted text may describe what kind of GitHub project a user wants.
    Your output must be strictly valid JSON with only these keys (omit if not found):
    - query
    - category

    Extract from the following text:
    ---
    {extracted_text}
    ---

    Output must be valid JSON with the structure:
    {{
        "query": "<query>",
        "category": "<category>"
    }}

    Query must be such that it can be used in a GitHub search query.
    Do not include small library or dependency names in the query.
    Do not include multiple of the technology in the search query.
    If required then use only one main technology in the query.
    Category must be a programming language.

    """

    raw_response = chat_with_llm(prompt)

    try:
        params = json.loads(raw_response)
        if not isinstance(params, dict):
            raise ValueError("LLM output is not a dictionary.")
    except Exception as e:
        raise ValueError(f"Failed to parse LLM output: {e}\nOutput was: {raw_response}")

    # Add static/default values
    static_params = {
        "limit": 3,
        "stars": ">10",
        "sort": "stars",
        "order": "desc",
        "token": github_token
    }

    return {**params, **static_params}
