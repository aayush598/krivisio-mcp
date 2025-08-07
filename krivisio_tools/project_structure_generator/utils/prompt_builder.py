from typing import List, Dict
from krivisio_tools.project_structure_generator.models.preferences import ProjectPreferences

def build_prompt(
    project_description: str,
    tech_stack: List[str],
    preferences: ProjectPreferences,
    similar_examples: List[Dict] = []
) -> str:
    """
    Builds a precise, strict prompt to instruct the LLM to generate a valid directory structure.
    """
    prompt_lines = []

    # Role and intent
    prompt_lines.append("You are an expert software architect specialized in clean and production-ready directory structures.")

    # Project context
    prompt_lines.append("\n🧠 Project Overview:")
    prompt_lines.append(f"Description: {project_description.strip()}")
    if tech_stack:
        tech_list = ", ".join(tech_stack)
        prompt_lines.append(f"Tech Stack: {tech_list}")

    # Preferences
    prompt_lines.append("\n⚙️ Preferences:")
    for k, v in preferences.to_dict().items():
        prompt_lines.append(f"- {k}: {v}")

    # Similar examples (optional)
    if similar_examples:
        prompt_lines.append("\n📁 Similar Examples:")
        for ex in similar_examples:
            prompt_lines.append(f"- Description: {ex['description']}")
            prompt_lines.append(f"  Tech Stack: {', '.join(ex['tech_stack'])}")
            prompt_lines.append(f"  Structure:\n  {ex['structure']}\n")

    # Formatting requirements
    prompt_lines.append("\n✅ Output Format (MUST FOLLOW STRICTLY):")
    prompt_lines.append("- Output ONLY a valid JSON object, without markdown or triple backticks.")
    prompt_lines.append("- Use ONLY the following keys: \"name\", \"type\", and \"children\".")
    prompt_lines.append("- Keys and all string values MUST be in double quotes.")
    prompt_lines.append("- `type` must be either \"file\" or \"folder\".")
    prompt_lines.append("- If `type` is \"folder\", include a `children` list.")
    prompt_lines.append("- Do NOT include any other metadata, explanation, notes, or comments.")
    prompt_lines.append("- Do NOT include any null values or fields like `_docs`.")

    # Add a small schema example
    prompt_lines.append("\n🧾 Example Schema:")
    prompt_lines.append('''{
  "name": "my-app",
  "type": "folder",
  "children": [
    {
      "name": "backend",
      "type": "folder",
      "children": [
        {
          "name": "main.py",
          "type": "file"
        }
      ]
    }
  ]
}''')

    prompt_lines.append("\n⛔ Output ONLY valid JSON. No markdown, comments, or backticks. No extra fields.")

    return "\n".join(prompt_lines)
