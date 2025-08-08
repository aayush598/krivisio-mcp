# github/update_repo.py

import os
import shutil
from git import Repo
from pathlib import Path
from typing import List, Tuple

def update_repo(
    git_url: str,
    branch: str,
    files_to_update: List[Tuple[str, str]],  # List of (relative_path, file_content)
    commit_message: str,
    token: str
) -> str:
    """
    Clones a repo, updates/adds files, commits, and pushes.

    Args:
        git_url (str): HTTPS URL of the repo (e.g., https://github.com/user/repo.git)
        branch (str): Branch to update.
        files_to_update (List[Tuple[str, str]]): List of file path and content.
        commit_message (str): Commit message.
        token (str): GitHub personal access token.

    Returns:
        str: The commit hash pushed to the repo.
    """
    # Insert token into URL for authentication
    auth_url = git_url.replace("https://", f"https://{token}@")
    tmp_dir = Path("./tmp_repo")

    # Cleanup if exists
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)

    try:
        # Clone the repo
        repo = Repo.clone_from(auth_url, tmp_dir, branch=branch)

        # Add or update files
        for file_path, content in files_to_update:
            full_path = tmp_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

        repo.git.add(all=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
        commit_hash = repo.head.commit.hexsha

        return commit_hash

    finally:
        # Clean up the temporary directory
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
