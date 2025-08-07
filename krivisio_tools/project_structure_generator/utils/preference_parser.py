from typing import Dict, Any
from models.preferences import ProjectPreferences


def parse_preferences(raw_input: Dict[str, Any]) -> ProjectPreferences:
    """
    Converts raw user input into a ProjectPreferences object.
    Applies defaults for missing or malformed fields.

    Args:
        raw_input (dict): Dictionary with potential keys like:
            - include_docs (bool)
            - include_tests (bool)
            - include_docker (bool)
            - include_ci_cd (bool)
            - custom_folders (list of str)
            - framework_specific (bool)

    Returns:
        ProjectPreferences: Parsed preferences object
    """
    return ProjectPreferences(
        include_docs=bool(raw_input.get("include_docs", True)),
        include_tests=bool(raw_input.get("include_tests", True)),
        include_docker=bool(raw_input.get("include_docker", False)),
        include_ci_cd=bool(raw_input.get("include_ci_cd", False)),
        custom_folders=raw_input.get("custom_folders", []) or [],
        framework_specific=bool(raw_input.get("framework_specific", True)),
    )
