"""
Combined onboarding functionality interface.

This module aggregates various onboarding-related document generation
functions such as proposal, quotation, contract, etc.

Currently supports:
- Proposal Generation
"""

from krivisio_tools.report_generation.app.routes.onboarding.proposal import generate_proposal_document


def generate_onboarding_document(doc_type: str, input_data: dict) -> str:
    """
    Dispatch onboarding document generation based on type.

    Args:
        doc_type (str): Type of document to generate (e.g., 'proposal')
        input_data (dict): Structured data required for document generation

    Returns:
        str: Generated document content from LLM

    Raises:
        ValueError: If the provided document type is unsupported
    """
    doc_type = doc_type.lower()

    if doc_type == "proposal":
        return generate_proposal_document(proposal_data=input_data)

    # Placeholder for future onboarding types
    # elif doc_type == "quotation":
    #     return generate_quotation_document(input_data)
    # elif doc_type == "contract":
    #     return generate_contract_document(input_data)

    raise ValueError(f"Unsupported onboarding document type: '{doc_type}'")
