# github/create_branch.py
from github import Github
import re

def extract_repo_name(repo_url: str) -> str:
    """
    Extracts the 'username/repo' part from a full GitHub repo URL.

    Args:
        repo_url (str): Full GitHub repository URL.

    Returns:
        str: Extracted repository name in 'username/repo' format.
    """
    match = re.search(r"github\.com[:/]+([^/]+/[^/]+?)(?:\.git)?$", repo_url)
    if not match:
        raise ValueError("Invalid GitHub repository URL.")
    return match.group(1)


def create_branch(token: str, repo_name: str, new_branch: str, source_branch: str = "main") -> str:
    """
    Creates a new branch from an existing one.

    Args:
        token (str): GitHub personal access token.
        repo_name (str): Full repo name (e.g., 'username/repo').
        new_branch (str): Name of the new branch to create.
        source_branch (str): Name of the source branch.

    Returns:
        str: Ref name of the created branch.
    """
    g = Github(token)
    repo_name = extract_repo_name(repo_name)
    repo = g.get_repo(repo_name)
    source_ref = repo.get_git_ref(f"heads/{source_branch}")
    repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=source_ref.object.sha)
    return f"refs/heads/{new_branch}"
