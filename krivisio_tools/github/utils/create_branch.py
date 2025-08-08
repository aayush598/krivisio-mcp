# github/create_branch.py
from github import Github

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
    repo = g.get_repo(repo_name)
    source_ref = repo.get_git_ref(f"heads/{source_branch}")
    repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=source_ref.object.sha)
    return f"refs/heads/{new_branch}"
