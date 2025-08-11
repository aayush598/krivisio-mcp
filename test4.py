from krivisio_tools.github.main import handle_github_action
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Optional: Testing different inputs
if __name__ == "__main__":
    import time

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
