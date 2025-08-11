# krivisio_tools/github/main.py

from krivisio_tools.github.utils.init_repo import init_repo
from krivisio_tools.github.utils.create_branch import create_branch
from krivisio_tools.github.utils.update_repo import update_repo
from krivisio_tools.github.utils.suggestions_techstack_features import process_document
from krivisio_tools.github.utils.setup_folder_structure import setup_github_folder_structure

def handle_github_action(input_data: dict):
    """
    Handles a GitHub action based on the input data.
    
    Expected structure:
    {
        "function": "init_repo" | "create_branch" | "update_repo",
        "data": { ... }  # parameters for the specific function
    }
    """
    function = input_data.get("function")
    data = input_data.get("data", {})

    if function == "init_repo":
        return init_repo(
            token=data["token"],
            repo_name=data["repo_name"],
            private=data.get("private", True),
            description=data.get("description", "")
        )

    elif function == "create_branch":
        return create_branch(
            token=data["token"],
            repo_name=data["repo_name"],
            new_branch=data["new_branch"],
            source_branch=data.get("source_branch", "main")
        )

    elif function == "update_repo":
        return update_repo(
            git_url=data["git_url"],
            branch=data["branch"],
            files_to_update=data["files_to_update"],
            commit_message=data["commit_message"],
            token=data["token"]
        )
    
    elif function == "process_document":
        return process_document(
            input_source=data["document_input"],
            source_type=data["document_type"],
            github_token=data["github_token"]
        )

    elif function == "setup_folder_structure":
        return setup_github_folder_structure(
            github_token=data["github_token"],
            repo_name=data["repo_name"],
            structure=data["structure"]
        )
    
    else:
        raise ValueError(f"Unsupported function: {function}")

