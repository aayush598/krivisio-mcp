# krivisio_tools/github/utils/search_repo.py

from github import Github
from typing import List, Dict, Any

def search_repo(user_input: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Searches GitHub repositories based on user input.

    Args:
        user_input (dict): Dictionary with possible keys:
            - token (str): GitHub personal access token (required)
            - query (str): Search query for repositories (required)
            - limit (int): Number of repositories to return (default=5)
            - category (str): Programming language or topic (optional)
            - stars (str): Star filter, e.g. '>100', '>=500' (optional)
            - sort (str): Sort field, one of 'stars', 'forks', 'updated' (optional)
            - order (str): 'desc' or 'asc' (default='desc')

    Returns:
        List[dict]: A list of dictionaries with repo details.
    """
    token = user_input.get("token")
    if not token:
        raise ValueError("GitHub token is required in user_input['token'].")

    query = user_input.get("query")
    if not query:
        raise ValueError("Search query is required in user_input['query'].")

    limit = user_input.get("limit", 5)
    category = user_input.get("category")
    stars = user_input.get("stars")
    sort = user_input.get("sort", None)
    order = user_input.get("order", "desc")

    # Build GitHub search query
    search_query = query
    if category:
        search_query += f" language:{category}"
    if stars:
        search_query += f" stars:{stars}"

    g = Github(token)
    results = g.search_repositories(query=search_query, sort=sort, order=order)

    repo_list = []
    for repo in results[:limit]:
        repo_list.append({
            "name": repo.name,
            "full_name": repo.full_name,
            "html_url": repo.html_url,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "language": repo.language,
            "updated_at": repo.updated_at.isoformat()
        })

    return repo_list
