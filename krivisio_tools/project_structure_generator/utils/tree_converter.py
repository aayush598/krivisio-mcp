from typing import Dict, List


def flatten_structure(
    structure: Dict,
    base_path: str = ""
) -> List[str]:
    """
    Flattens the nested directory structure into a list of path strings.

    Args:
        structure (dict): Directory tree from LLM.
        base_path (str): Internal use – recursive base path.

    Returns:
        List[str]: List of full paths like ['my-app/README.md', 'my-app/src/index.js']
    """
    paths = []
    current_path = f"{base_path}/{structure['name']}".lstrip("/")

    if structure["type"] == "file":
        paths.append(current_path)
    elif structure["type"] == "folder":
        paths.append(current_path + "/")  # optionally keep trailing slash
        children = structure.get("children", [])
        for child in children:
            paths.extend(flatten_structure(child, current_path))
    return paths


def extract_files_only(
    structure: Dict,
    base_path: str = ""
) -> List[str]:
    """
    Extracts only file paths from the structure.

    Args:
        structure (dict): Directory tree
        base_path (str): Recursive internal path

    Returns:
        List[str]: All file paths
    """
    if structure["type"] == "file":
        return [f"{base_path}/{structure['name']}".lstrip("/")]
    
    files = []
    current_path = f"{base_path}/{structure['name']}".lstrip("/")
    for child in structure.get("children", []):
        files.extend(extract_files_only(child, current_path))
    return files


def extract_folders_only(
    structure: Dict,
    base_path: str = ""
) -> List[str]:
    """
    Extracts only folder paths from the structure.

    Args:
        structure (dict): Directory tree
        base_path (str): Recursive internal path

    Returns:
        List[str]: All folder paths
    """
    folders = []
    if structure["type"] == "folder":
        current_path = f"{base_path}/{structure['name']}".lstrip("/")
        folders.append(current_path + "/")
        for child in structure.get("children", []):
            folders.extend(extract_folders_only(child, current_path))
    return folders
