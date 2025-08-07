import json
from typing import Union, Dict, List
# from krivisio_tools.project_structure_generator.utils.json_cleaner import clean_llm_json_response
from krivisio_tools.project_structure_generator.utils.json_cleaner import sanitize_and_parse_json

def parse_llm_output(response_text: str) -> Union[Dict, None]:
    """
    Attempts to parse the LLM's JSON directory structure output.

    Args:
        response_text (str): Raw text from the LLM.

    Returns:
        dict: Parsed directory structure if valid, otherwise None.
    """
    print(f"response_text : {response_text}")
    
    # Attempt to sanitize and parse
    parsed = sanitize_and_parse_json(response_text)
    
    if not parsed:
        print("❌ Failed to parse JSON from LLM output.")
        return None

    if is_valid_structure(parsed):
        return parsed
    else:
        print("❌ Parsed structure is invalid.")
        return None


def is_valid_structure(structure: Dict) -> bool:
    """
    Recursively validates that the structure follows expected schema:
    - Each node must have: name (str), type ('file' or 'folder')
    - If type == 'folder', must optionally include 'children': list

    Args:
        structure (dict): Structure to validate

    Returns:
        bool: True if structure is valid
    """
    if not isinstance(structure, dict):
        return False

    if "name" not in structure or "type" not in structure:
        return False

    if structure["type"] not in ("file", "folder"):
        return False

    if structure["type"] == "folder":
        children = structure.get("children", [])
        if not isinstance(children, list):
            return False
        for child in children:
            if not is_valid_structure(child):
                return False

    return True


def pretty_print_structure(structure: Dict, indent: int = 0) -> None:
    """
    Prints the directory structure in a tree-like format.

    Args:
        structure (dict): Directory structure
        indent (int): Current indentation level
    """
    prefix = "  " * indent
    name = structure.get("name", "[Unnamed]")
    type_ = structure.get("type", "[Unknown]")

    print(f"{prefix}- {name}/" if type_ == "folder" else f"{prefix}- {name}")

    if type_ == "folder":
        for child in structure.get("children", []):
            pretty_print_structure(child, indent + 1)
