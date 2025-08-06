"""
Proposal generation logic for onboarding phase.
Calls template renderer and LLM client for generation.
"""

from krivisio_tools.report_generation.app.utils.template_helpers import render_template
from krivisio_tools.report_generation.app.utils.llm_client import chat_with_llm


def generate_proposal_document(proposal_data: dict) -> str:
    """
    Generates a full proposal specification document using a template
    and an LLM model.

    Args:
        proposal_data (dict): Dictionary containing:
            - project_name (str)
            - complexity_level (str)
            - features (List[str])
            - cocomo_results (Dict)

    Returns:
        str: Generated proposal document content from LLM.
    """
    # Step 1: Render prompt from template
    prompt = render_template(template_name="proposal", input_data=proposal_data)

    # Step 2: Send prompt to LLM
    llm_response = chat_with_llm(prompt=prompt)

    return llm_response
