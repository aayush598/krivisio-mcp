# krivisio_tools/github/orchestrator.py

from typing import Literal, Dict, Any, List
from krivisio_tools.github.utils.extract_text import extract_text
from krivisio_tools.github.utils.extract_search_params import extract_search_params_from_text
from krivisio_tools.github.utils.search_repo import search_repo
from krivisio_tools.github.utils.extract_repo_features import extract_features_and_stack
from krivisio_tools.github.utils.classify_repo_features import classify_features_and_tech_stack


def process_document(
    input_source: str,
    source_type: Literal["text", "pdf", "docx", "txt"],
    github_token: str
) -> Dict[str, Any]:
    """
    Full pipeline to process a document, search GitHub, extract and classify features.

    Args:
        input_source (str): File path or text depending on source_type.
        source_type (Literal): "text", "pdf", "docx", or "txt".
        github_token (str): GitHub personal access token.

    Returns:
        dict: {
            "search_params": {...},
            "repos": [...],
            "repo_features": {...},
            "classified_features": {...}
        }
    """
    # 1. Extract text
    extracted_text = extract_text(input_source, source_type)

    # 2. Extract search parameters
    search_params = extract_search_params_from_text(extracted_text, github_token)

    # 3. Search for repos
    repos = search_repo(search_params)

    # 4. Extract features & tech stack
    repo_links = [repo["html_url"] for repo in repos]
    repo_features = extract_features_and_stack(github_token, repo_links)

    # 5. Classify features & tech stack
    classified_features = classify_features_and_tech_stack(repo_features)

    return {
        "search_params": search_params,
        "repos": repos,
        "repo_features": repo_features,
        "classified_features": classified_features
    }
