"""
Utility for dynamically invoking registered document templates
based on template name and standardized input.
"""

from typing import Callable, Dict
from pydantic import BaseModel
from krivisio_tools.report_generation.templates.onboarding import proposal

# Define the type of input expected for all templates
TemplateInput = BaseModel

# Registry to map template names to their corresponding builder functions
TEMPLATE_REGISTRY: Dict[str, Callable[[TemplateInput], str]] = {
    "proposal": proposal.build_proposal_spec_prompt,
    # Future templates can be added here
    # "sow": sow.build_sow_document_prompt,
    # "nda": nda.build_nda_prompt,
}


def render_template(template_name: str, input_data: TemplateInput) -> str:
    """
    Render a document prompt based on the specified template.

    Args:
        template_name (str): Key identifying which template to use (e.g., "proposal").
        input_data (TemplateInput): A Pydantic model instance with required input data.

    Returns:
        str: The generated document prompt or content.

    Raises:
        ValueError: If the specified template is not found in the registry.
    """
    template_func = TEMPLATE_REGISTRY.get(template_name.lower())
    if not template_func:
        raise ValueError(f"Template '{template_name}' is not registered.")

    return template_func(input_data)
