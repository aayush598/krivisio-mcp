from typing import List, Dict, Optional
from krivisio_tools.project_structure_generator.models.preferences import ProjectPreferences
from krivisio_tools.project_structure_generator.services.llm_service import generate_directory_structure
from krivisio_tools.project_structure_generator.services.cache_service import get_from_cache, save_to_cache
from krivisio_tools.project_structure_generator.services.similarity_service import find_similar_examples
from krivisio_tools.project_structure_generator.services.validation_service import validate_structure


def run_structure_generation_agent(
    project_description: str,
    tech_stack: List[str],
    preferences: ProjectPreferences,
    use_cache: bool = True,
    use_similarity: bool = True
) -> Optional[Dict]:
    """
    Main agent function that coordinates the generation process.

    Args:
        project_description (str): Description of the user’s project.
        tech_stack (List[str]): Tech/frameworks in use.
        preferences (ProjectPreferences): User preferences.
        use_cache (bool): Whether to reuse cached results.
        use_similarity (bool): Whether to use similar examples in prompt.

    Returns:
        dict | None: Directory structure or None if generation failed.
    """
    # Convert preferences for cache key
    pref_dict = preferences.to_dict()

    # Step 1: Check cache
    if use_cache:
        cached_result = get_from_cache(project_description, tech_stack, pref_dict)
        if cached_result:
            print("⚡ Loaded from cache.")
            return cached_result

    # Step 2: Retrieve similar examples
    examples = find_similar_examples(project_description) if use_similarity else []

    # Step 3: Generate structure
    structure = generate_directory_structure(
        project_description=project_description,
        tech_stack=tech_stack,
        preferences=preferences,
        examples=examples
    )

    # Step 4: Validate structure
    if structure and validate_structure(structure):
        # Step 5: Cache it for future use
        if use_cache:
            save_to_cache(project_description, tech_stack, pref_dict, structure)
        return structure
    else:
        print("❌ Structure generation failed or was invalid.")
        return None
