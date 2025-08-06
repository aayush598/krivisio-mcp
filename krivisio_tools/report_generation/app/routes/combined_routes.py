"""
Centralized dispatcher for routing functionality across different modules.

Currently supported modules:
- Onboarding

Future expansions may include:
- Reporting
- Compliance
- Project Tracking
"""

from krivisio_tools.report_generation.app.routes.onboarding.combined_onboarding import generate_onboarding_document


def route_document_generation(module: str, doc_type: str, input_data: dict) -> str:
    """
    Dispatch document generation across functional modules.

    Args:
        module (str): The functional module (e.g., 'onboarding')
        doc_type (str): The specific document type within the module (e.g., 'proposal')
        input_data (dict): Input data needed for template rendering and LLM generation

    Returns:
        str: Final generated document

    Raises:
        ValueError: If the module or document type is unsupported
    """
    module = module.lower()

    if module == "onboarding":
        return generate_onboarding_document(doc_type=doc_type, input_data=input_data)

    # Future module routing examples
    # elif module == "reporting":
    #     return generate_reporting_document(doc_type, input_data)
    # elif module == "compliance":
    #     return generate_compliance_document(doc_type, input_data)

    raise ValueError(f"Unsupported module: '{module}'")
