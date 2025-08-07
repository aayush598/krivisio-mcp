from typing import Dict, List


def is_valid_structure(node: Dict) -> bool:
    """
    Recursively validates the directory structure returned by the LLM.

    Args:
        node (dict): A file or folder node.

    Returns:
        bool: True if the structure is valid, False otherwise.
    """
    if not isinstance(node, dict):
        return False

    if "name" not in node or "type" not in node:
        return False

    if node["type"] not in ["file", "folder"]:
        return False

    if not isinstance(node["name"], str) or not node["name"]:
        return False

    if node["type"] == "folder":
        if "children" not in node:
            return False
        if not isinstance(node["children"], list):
            return False
        for child in node["children"]:
            if not is_valid_structure(child):
                return False

    return True


def validate_structure(tree: Dict) -> bool:
    """
    Wrapper to validate the root of the directory tree.

    Args:
        tree (dict): Full directory structure.

    Returns:
        bool: True if valid, False otherwise.
    """
    return is_valid_structure(tree)
