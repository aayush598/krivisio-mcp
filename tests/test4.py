from krivisio_tools.github.main import handle_github_action
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    username = "aayush598"
    timestamp = int(time.time())
    repo_name = f"test-repo-{timestamp}"

    # 👇 Test repo creation
    init_input = {
        "function": "init_repo",
        "data": {
            "token": token,
            "repo_name": repo_name,
            "private": True,
            "description": "Test repo created via automation"
        }
    }
    print("Creating repo...")
    repo_url = handle_github_action(init_input)
    print(f"Repo URL: {repo_url}")

    # 👇 Test branch creation
    branch_input = {
        "function": "create_branch",
        "data": {
            "token": token,
            "repo_name": f"https://www.github.com/{username}/{repo_name}",
            "new_branch": "feature/test-branch"
        }
    }
    print("Creating branch...")
    branch_ref = handle_github_action(branch_input)
    print(f"Branch created: {branch_ref}")

    # 👇 Test folder structure setup
    folder_structure_input = {
        "function": "setup_folder_structure",
        "data": {
            "github_token": token,
            "repo_name": f"https://github.com/{username}/{repo_name}",
            "structure": {
                "name": repo_name,
                "type": "folder",
                "children": [
                    {"name": "assets", "type": "folder", "children": []},
                    {"name": "utils", "type": "folder", "children": []},
                    {
                        "name": "src",
                        "type": "folder",
                        "children": [
                            {"name": "index.html", "type": "file"},
                            {"name": "styles.css", "type": "file"},
                            {"name": "app.js", "type": "file"}
                        ]
                    },
                    {
                        "name": "docs",
                        "type": "folder",
                        "children": [
                            {"name": "README.md", "type": "file"}
                        ]
                    }
                ]
            }
        }
    }
    print("Setting up folder structure...")
    folder_setup_result = handle_github_action(folder_structure_input)
    print(f"Folder structure created: {folder_setup_result}")

    # 👇 Test repo update
    update_input = {
        "function": "update_repo",
        "data": {
            "token": token,
            "git_url": f"https://github.com/{username}/{repo_name}.git",
            "branch": "feature/test-branch",
            "files_to_update": [
                ("src/main.py", "print('Hello from main.py')"),
                ("src/utils/helpers.py", "# Utility functions")
            ],
            "commit_message": "Added project files"
        }
    }
    print("Updating repo...")
    commit_sha = handle_github_action(update_input)
    print(f"Commit SHA: {commit_sha}")
