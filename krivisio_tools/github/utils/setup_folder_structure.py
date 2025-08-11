import os
import re
import shutil
from github import Github
from typing import Dict


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


def create_structure_local(base_path: str, structure: Dict):
    """
    Recursively create folder and file structure locally.
    
    Args:
        base_path (str): Path where structure should be created.
        structure (dict): Structure in JSON format.
    """
    path = os.path.join(base_path, structure["name"])

    if structure["type"] == "folder":
        os.makedirs(path, exist_ok=True)
        for child in structure.get("children", []):
            create_structure_local(path, child)
    elif structure["type"] == "file":
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("")  # create empty file


def upload_structure_to_github(repo, base_path: str, github_path: str = ""):
    """
    Upload local folder structure to GitHub.
    
    Args:
        repo: GitHub repo object.
        base_path (str): Local base folder path.
        github_path (str): Path inside the repo.
    """
    for root, dirs, files in os.walk(base_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, base_path)
            github_file_path = os.path.join(github_path, relative_path).replace("\\", "/")

            with open(local_file_path, "r", encoding="utf-8") as f:
                content = f.read()

            try:
                repo.create_file(github_file_path, f"Add {github_file_path}", content)
                print(f"✅ Created: {github_file_path}")
            except Exception as e:
                print(f"⚠️ Skipped {github_file_path}: {e}")


def setup_github_folder_structure(github_token: str, repo_name: str, structure: Dict):
    """
    Main function to set up folder structure in a GitHub repo.
    
    Args:
        github_token (str): Personal access token.
        repo_url_or_name (str): GitHub repo name (username/repo) or full URL.
        structure (dict): JSON structure of folders/files.
    """
    temp_dir = "temp_project_structure"

    # Handle full URL case
    if repo_name.startswith("http"):
        repo_name = extract_repo_name(repo_name)

    # Create locally
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    create_structure_local(temp_dir, structure)

    # Upload to GitHub
    g = Github(github_token)
    repo = g.get_repo(repo_name)

    project_folder = os.path.join(temp_dir, structure["name"])
    upload_structure_to_github(repo, project_folder)

    # Cleanup
    shutil.rmtree(temp_dir)
