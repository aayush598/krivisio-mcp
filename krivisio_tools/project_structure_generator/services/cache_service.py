import hashlib
import json
from typing import Dict, Optional


# In-memory cache (simple Python dict)
_cache: Dict[str, Dict] = {}


def _generate_cache_key(
    project_description: str,
    tech_stack: list,
    preferences: dict
) -> str:
    """
    Generates a unique hash key based on input.

    Args:
        project_description (str): Project description.
        tech_stack (list): List of tech/frameworks.
        preferences (dict): Preferences as dictionary.

    Returns:
        str: Hash key for cache lookup.
    """
    raw = json.dumps({
        "description": project_description.strip(),
        "tech_stack": sorted(tech_stack),
        "preferences": preferences
    }, sort_keys=True)

    return hashlib.sha256(raw.encode()).hexdigest()


def get_from_cache(
    project_description: str,
    tech_stack: list,
    preferences: dict
) -> Optional[Dict]:
    """
    Returns a cached structure if available.

    Returns:
        dict or None
    """
    key = _generate_cache_key(project_description, tech_stack, preferences)
    return _cache.get(key)


def save_to_cache(
    project_description: str,
    tech_stack: list,
    preferences: dict,
    structure: Dict
) -> None:
    """
    Saves a generated structure to cache.
    """
    key = _generate_cache_key(project_description, tech_stack, preferences)
    _cache[key] = structure
