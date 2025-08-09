# krivisio_tools/github/utils/search_repo.py

from github import Github
from typing import List, Dict, Any

# krivisio_tools/github/utils/search_repo.py

def search_repo(params: dict):
    token = params["token"]
    g = Github(token)

    query = params.get("query", "")
    category = params.get("category")
    stars = params.get("stars")
    limit = params.get("limit", 5)  # default 5 repos
    sort = params.get("sort", "stars")  # default sort by stars
    order = params.get("order", "desc")  # default order

    # Construct the GitHub search query
    search_query = query
    if category:
        search_query += f" language:{category}"
    if stars:
        search_query += f" stars:{stars}"

    results = g.search_repositories(query=search_query, sort=sort, order=order)

    repos = []
    for repo in results[:limit]:
        repos.append({
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "language": repo.language,
            "html_url": repo.html_url
        })

    return repos
