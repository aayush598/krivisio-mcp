# krivisio_tools/github/utils/extract_repo_features.py

from typing import List, Dict
from github import Github
from krivisio_tools.github.utils.llm_client import chat_with_llm
import json

def get_readme_content(token: str, repo_full_name: str) -> str:
    """
    Fetches the README.md content for a given GitHub repository.

    Args:
        token (str): GitHub personal access token.
        repo_full_name (str): Repo full name (e.g., 'username/repo').

    Returns:
        str: README content in plain text.
    """
    g = Github(token)
    repo = g.get_repo(repo_full_name)

    try:
        readme = repo.get_readme()
        return readme.decoded_content.decode("utf-8")
    except Exception as e:
        raise ValueError(f"Could not fetch README for {repo_full_name}: {e}")


def analyze_repo_with_llm(readme_content: str) -> Dict[str, List[str]]:
    """
    Sends the README content to the LLM to extract features and tech stacks.

    Args:
        readme_content (str): Text of the README.md.

    Returns:
        dict: Contains 'features' and 'tech_stack' lists.
    """
    prompt = f"""
    You are a system that extracts key project details from a GitHub README file.
    From the following README content, extract:
    1. Features: A concise bullet list of main features.
    2. Tech Stack: A bullet list of programming languages, frameworks, and tools used.

    Output must be valid JSON with the structure:
    {{
        "features": ["feature1", "feature2", ...],
        "tech_stack": ["tech1", "tech2", ...]
    }}

    README content:
    ---
    {readme_content}
    ---
    """

    raw_response = chat_with_llm(prompt)

    try:
        data = json.loads(raw_response)  # You can replace with json.loads if strictly JSON
        if not isinstance(data, dict) or "features" not in data or "tech_stack" not in data:
            raise ValueError("Invalid LLM output structure.")
        return data
    except Exception as e:
        raise ValueError(f"Error parsing LLM output: {e}\nOutput was: {raw_response}")


def extract_features_and_stack(token: str, repo_links: List[str]) -> Dict[str, Dict[str, List[str]]]:
    """
    For each repo link, fetch README and extract features and tech stack.

    Args:
        token (str): GitHub personal access token.
        repo_links (List[str]): List of full GitHub repo URLs.

    Returns:
        dict: Mapping of repo_full_name -> {'features': [...], 'tech_stack': [...]}
    """
    results = {}
    for link in repo_links:
        # Extract "username/repo" from link
        try:
            parts = link.rstrip("/").split("/")
            repo_full_name = f"{parts[-2]}/{parts[-1]}"
        except IndexError:
            raise ValueError(f"Invalid GitHub repo link: {link}")

        readme_content = get_readme_content(token, repo_full_name)
        analysis = analyze_repo_with_llm(readme_content)
        results[repo_full_name] = analysis

    return results
