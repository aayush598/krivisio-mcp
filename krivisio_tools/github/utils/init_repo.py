# github/init_repo.py
from github import Github

def init_repo(token: str, repo_name: str, private: bool = True, description: str = "") -> str:
    """
    Initializes a new GitHub repository and commits a basic README.md file.

    Args:
        token (str): GitHub personal access token.
        repo_name (str): Name of the repository.
        private (bool): Whether the repo is private.
        description (str): Description of the repo.

    Returns:
        str: URL of the created repository.
    """
    g = Github(token)
    user = g.get_user()
    repo = user.create_repo(name=repo_name, private=private, description=description)

    # Add a basic README.md file to the main branch
    readme_content = f"# {repo_name}\n\n{description or 'This is a new repository.'}"
    repo.create_file(
        path="README.md",
        message="Initial commit with README",
        content=readme_content,
        branch="main"
    )

    return repo.html_url
