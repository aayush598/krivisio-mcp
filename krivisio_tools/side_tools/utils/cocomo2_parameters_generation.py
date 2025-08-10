import json
from krivisio_tools.side_tools.utils.llm_client import chat_with_llm, strip_code_fences

def generate_cocomo2_parameters(project_idea: str, level: str, features: list[str], tech_stacks: list[str]) -> dict:
    """
    Generate realistic COCOMO-II parameters based on project details, features, and tech stacks.

    Args:
        project_idea (str): Short description of the project.
        level (str): Complexity level ("basic", "intermediate", "advanced").
        features (list[str]): List of key features to implement.
        tech_stacks (list[str]): List of technologies/languages to use.

    Returns:
        dict: Generated COCOMO-II parameters.
    """
    
    features_text = "\n".join(f"- {f}" for f in features)
    tech_text = ", ".join(tech_stacks)

    prompt = f"""
You are a software estimation expert with deep knowledge of the COCOMO-II methodology.
Based on the project details below, generate realistic and consistent input parameters for ALL four COCOMO-II sections.

**Project Details:**
- Project Idea: {project_idea}
- Complexity Level: {level}
- Features:
{features_text}
- Tech Stacks: {tech_text}

**IMPORTANT:**
Output must strictly follow this JSON structure and value constraints:

1. "function_points":
    - "fp_items": list of objects with:
        - fp_type: one of "EI", "EO", "EQ", "ILF", "EIF"
        - det: integer > 0
        - ftr_or_ret: integer > 0
    - "language": programming language string (from provided tech stack, else pick common match)
2. "reuse":
    - asloc: integer
    - dm, cm, im: integers 0-100
    - su_rating: one of "VL", "L", "N", "H", "VH"
    - aa_rating: one of '0', '2', '4', '6' or '8'
    - unfm_rating: one of "CF", "MF", "SF", "CFa", "MU", "CU"
    - at: integer 0-100
3. "revl":
    - new_sloc: integer
    - adapted_esloc: integer
    - revl_percent: integer (0-100)
4. "effort_schedule":
    - sloc_ksloc: decimal
    - sced_rating: one of "VL", "L", "N", "H", "VH"

**Complexity guidance:**
- Basic: 1-5 KSLOC, higher reuse, simple tech
- Intermediate: 5-20 KSLOC, moderate reuse
- Advanced: 20+ KSLOC, lower reuse, complex tech

Respond ONLY with valid JSON in this format:
{{
  "function_points": {{
    "fp_items": [
      {{"fp_type": "EI", "det": 8, "ftr_or_ret": 1}},
      {{"fp_type": "EO", "det": 10, "ftr_or_ret": 2}}
    ],
    "language": "Java"
  }},
  "reuse": {{
    "asloc": 3500,
    "dm": 20,
    "cm": 10,
    "im": 10,
    "su_rating": "L",
    "aa_rating": "2",
    "unfm_rating": "N",
    "at": 15
  }},
  "revl": {{
    "new_sloc": 8500,
    "adapted_esloc": 2500,
    "revl_percent": 25
  }},
  "effort_schedule": {{
    "sloc_ksloc": 7.5,
    "sced_rating": "L"
  }}
}}
"""

    raw = chat_with_llm(prompt)
    cleaned = strip_code_fences(raw)

    try:
        params = json.loads(cleaned)
        return params
    except json.JSONDecodeError:
        # Fallback defaults if LLM output is invalid
        defaults = {
            "basic": {
                "function_points": {
                    "fp_items": [
                        {"fp_type": "EI", "det": 10, "ftr_or_ret": 2},
                        {"fp_type": "EO", "det": 8, "ftr_or_ret": 2},
                        {"fp_type": "ILF", "det": 15, "ftr_or_ret": 3}
                    ],
                    "language": tech_stacks[0] if tech_stacks else "Python"
                },
                "reuse": {
                    "asloc": 1000, "dm": 10, "cm": 15, "im": 5,
                    "su_rating": "H", "aa_rating": "2", "unfm_rating": "CF", "at": 10
                },
                "revl": {
                    "new_sloc": 3000, "adapted_esloc": 1000, "revl_percent": 10
                },
                "effort_schedule": {
                    "sloc_ksloc": 4.0, "sced_rating": "N"
                }
            },
            "intermediate": {
                "function_points": {
                    "fp_items": [
                        {"fp_type": "EI", "det": 15, "ftr_or_ret": 3},
                        {"fp_type": "EO", "det": 12, "ftr_or_ret": 3},
                        {"fp_type": "EQ", "det": 8, "ftr_or_ret": 2},
                        {"fp_type": "ILF", "det": 25, "ftr_or_ret": 4}
                    ],
                    "language": tech_stacks[0] if tech_stacks else "Java"
                },
                "reuse": {
                    "asloc": 3000, "dm": 20, "cm": 25, "im": 15,
                    "su_rating": "N", "aa_rating": "3", "unfm_rating": "MF", "at": 5
                },
                "revl": {
                    "new_sloc": 8000, "adapted_esloc": 3000, "revl_percent": 15
                },
                "effort_schedule": {
                    "sloc_ksloc": 11.0, "sced_rating": "N"
                }
            },
            "advanced": {
                "function_points": {
                    "fp_items": [
                        {"fp_type": "EI", "det": 25, "ftr_or_ret": 4},
                        {"fp_type": "EO", "det": 20, "ftr_or_ret": 4},
                        {"fp_type": "EQ", "det": 15, "ftr_or_ret": 3},
                        {"fp_type": "ILF", "det": 35, "ftr_or_ret": 5},
                        {"fp_type": "EIF", "det": 18, "ftr_or_ret": 3}
                    ],
                    "language": tech_stacks[0] if tech_stacks else "C++"
                },
                "reuse": {
                    "asloc": 5000, "dm": 35, "cm": 40, "im": 25,
                    "su_rating": "L", "aa_rating": "4", "unfm_rating": "CU", "at": 0
                },
                "revl": {
                    "new_sloc": 20000, "adapted_esloc": 5000, "revl_percent": 25
                },
                "effort_schedule": {
                    "sloc_ksloc": 25.0, "sced_rating": "H"
                }
            }
        }
        return defaults.get(level.lower(), defaults["intermediate"])
