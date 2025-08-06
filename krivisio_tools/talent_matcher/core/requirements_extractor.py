import json
from typing import Dict

from krivisio_tools.talent_matcher.config import (
    DEFAULT_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)

from krivisio_tools.talent_matcher.utils.llm_client import chat_with_llm


def extract_requirements_from_spec(spec_data: dict) -> Dict:
    """
    Uses the OpenAI API (via llm_client) to extract tech stack and team requirements.
    
    Args:
        spec_data (dict): The input spec document as a dictionary.

    Returns:
        Dict: Extracted tech stack, avg team size, and manager score threshold.
    """
    prompt = f"""
PROJECT SPECIFICATION DOCUMENT (JSON):
{json.dumps(spec_data, indent=2)}

INSTRUCTIONS:
1. Analyze the technical architecture and technology stack sections
2. Extract all mentioned technologies and group them by domain
3. Estimate team size based on project scope and timeline
4. Return JSON with tech stack and team requirements

OUTPUT FORMAT (raw JSON only, no markdown):
{{
    "tech_stack": {{
        "frontend": ["React", "TypeScript"],
        "backend": ["Node.js", "Express"],
        "database": ["PostgreSQL"],
        "devops": ["Docker", "Kubernetes"]
    }},
    "avg_team_size": 4.5,
    "manager_score_threshold": 4.0
}}
"""

    try:
        response = chat_with_llm(
            prompt=prompt,
            model=DEFAULT_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        return json.loads(response)

    except Exception as e:
        print(f"[LLM ERROR] Failed to extract requirements: {e}")
        # You may want to handle fallback differently in production
        return {
            "tech_stack": {
                "frontend": ["React"],
                "backend": ["Node.js"],
                "database": ["MySQL"]
            },
            "avg_team_size": 3.0,
            "manager_score_threshold": 4.0
        }
