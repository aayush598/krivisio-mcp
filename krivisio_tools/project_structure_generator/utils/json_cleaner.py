import json
import re
from typing import Any, Optional

from krivisio_tools.project_structure_generator.utils.llm_client import chat_with_llm


def sanitize_and_parse_json(text: str) -> Optional[Any]:
    """
    Attempts to sanitize and parse JSON content. Uses regex cleanup first,
    then falls back to LLM to auto-correct malformed JSON if needed.
    """
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try regex-based cleaning
    try:
        cleaned = re.sub(r"```(?:json)?", "", text)
        cleaned = cleaned.strip("` \n")

        cleaned = re.sub(r"'", '"', cleaned)
        cleaned = re.sub(r'"[a-zA-Z0-9_]*"\s*([a-zA-Z0-9_]+)\s*:', lambda m: f'"{m.group(1)}":', cleaned)
        cleaned = re.sub(r'(?<=[{,])\s*([a-zA-Z0-9_]+)\s*:', r'"\1":', cleaned)

        cleaned = re.sub(
            r':\s*([a-zA-Z_][a-zA-Z0-9_\-./]*)(?=\s*[,}])',
            lambda m: f': "{m.group(1)}"',
            cleaned
        )

        cleaned = re.sub(r'"\s*:\s*([a-zA-Z0-9_./\-]+)(?=\s*[,}])', r'": "\1"', cleaned)
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)

        return json.loads(cleaned)
    except Exception:
        pass  # Proceed to LLM fallback

    # Fallback: Use LLM to fix the structure
    try:
        prompt = f"""
You are a strict JSON repair assistant.

The following string is intended to be a **valid JSON object** that describes a file/folder structure, but it contains common formatting issues such as:
- Unquoted keys or string values
- Single quotes instead of double quotes
- Trailing commas
- Comments or markdown formatting (e.g., ```json)
- Invalid nesting or incomplete syntax

Your task:
1. Fix all issues in the JSON.
2. Ensure the result strictly complies with the JSON standard.
3. Return **only the corrected JSON string**, without any markdown, explanation, or commentary.

Broken JSON:
{text}
"""

        llm_fixed = chat_with_llm(prompt)
        print(f"LLM fixed JSON: {llm_fixed}")
        return json.loads(llm_fixed)
    except Exception as e:
        print(f"❌ JSON parsing failed after LLM fix: {e}")
        return None
