"""
Main module for document generation via combined routes.

Provides callable entry point for MCP or standalone execution.
"""

from typing import Dict, Any
from krivisio_tools.report_generation.app.routes.combined_routes import route_document_generation


def run_generation(module: str, doc_type: str, input_data: Dict[str, Any]) -> str:
    """
    Generate a document based on module and document type.

    Args:
        module (str): Functional module name (e.g., 'onboarding').
        doc_type (str): Document type within the module (e.g., 'proposal').
        input_data (Dict[str, Any]): Input data required for generation.

    Returns:
        str: Generated document.

    Raises:
        Exception: If routing or generation fails.
    """
    return route_document_generation(module=module, doc_type=doc_type, input_data=input_data)