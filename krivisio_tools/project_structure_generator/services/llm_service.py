from typing import List, Dict, Optional
from krivisio_tools.project_structure_generator.models.preferences import ProjectPreferences
from krivisio_tools.project_structure_generator.utils.prompt_builder import build_prompt
from krivisio_tools.project_structure_generator.utils.llm_client import chat_with_llm
from krivisio_tools.project_structure_generator.utils.output_parser import parse_llm_output


def generate_directory_structure(
    project_description: str,
    features: List[str],
    tech_stack: List[str],
    preferences: ProjectPreferences,
    examples: Optional[List[Dict]] = None
) -> Optional[Dict]:
    """
    Main service to generate a directory structure using an LLM.

    Args:
        project_description (str): The user’s project summary.
        tech_stack (List[str]): List of technologies/frameworks.
        preferences (ProjectPreferences): User customization.
        examples (Optional[List[Dict]]): Similar example structures for context.

    Returns:
        dict | None: Parsed directory tree or None on failure.
    """
    # 1. Build the prompt
    prompt = build_prompt(
        project_description=project_description,
        features=features,
        tech_stack=tech_stack,
        preferences=preferences,
        similar_examples=examples or []
    )

    # 2. Query the LLM
    response_text = chat_with_llm(prompt)

    # 3. Parse and validate the result
    structure = parse_llm_output(response_text)

    if structure:
        return structure
    else:
        print("⚠️ LLM returned an invalid structure.")
        return None
