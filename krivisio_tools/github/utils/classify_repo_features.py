# krivisio_tools/github/utils/classify_repo_features.py

from typing import Dict, Any
from krivisio_tools.github.utils.llm_client import chat_with_llm


def classify_features_and_tech_stack(repos_data: Dict[str, Dict[str, list]]) -> Dict[str, Any]:
    """
    Classifies features and tech stacks from multiple repositories into
    Basic, Intermediate, and Advanced categories.

    Args:
        repos_data (dict):
            {
                "repo_name": {
                    "features": [...],
                    "tech_stack": [...]
                },
                ...
            }

    Returns:
        dict: JSON-like structure:
        {
            "Basic": {
                "features": [...],
                "tech_stack": [...]
            },
            "Intermediate": {
                "features": [...],
                "tech_stack": [...]
            },
            "Advanced": {
                "features": [...],
                "tech_stack": [...]
            }
        }
    """
    prompt = f"""
    You are an AI that classifies GitHub repository features and tech stacks
    into three categories: Basic, Intermediate, and Advanced.

    Rules:
    - Basic: Beginner-friendly, minimal setup, simple functionality.
    - Intermediate: More complex, requires some programming knowledge, involves
      multiple components or moderate setup.
    - Advanced: High complexity, cutting-edge, scalable, heavy infrastructure or
      advanced algorithms.

    Input data (from multiple repositories):
    {repos_data}

    Output must be strictly valid JSON with the following structure:
    {{
        "Basic": {{
            "features": ["feature1", "feature2", ...],
            "tech_stack": ["tech1", "tech2", ...]
        }},
        "Intermediate": {{
            "features": ["feature1", "feature2", ...],
            "tech_stack": ["tech1", "tech2", ...]
        }},
        "Advanced": {{
            "features": ["feature1", "feature2", ...],
            "tech_stack": ["tech1", "tech2", ...]
        }}
    }}
    Do not include any explanations — output JSON only.
    """

    raw_response = chat_with_llm(prompt)

    try:
        data = eval(raw_response)  # You can replace with json.loads for safety
        if not all(k in data for k in ["Basic", "Intermediate", "Advanced"]):
            raise ValueError("Missing required categories in output.")
        return data
    except Exception as e:
        raise ValueError(f"Error parsing LLM output: {e}\nOutput was: {raw_response}")
