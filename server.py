#!/usr/bin/env python3
"""
MCP Integration for Krivisio Tools

This server integrates multiple tools under the MCP (Modular Control Platform) environment.

Tools Registered:
- Project Estimation Tool (COCOMO II, etc.)
- Report Generation Tool (Proposal generation and more)

Each tool follows a structured contract and can be extended independently.

Author: Aayush Gid
"""

from typing import Dict, Any, List

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from krivisio_tools.project_evaluation.main import run_estimation
from krivisio_tools.report_generation.app.main import run_generation
from krivisio_tools.talent_matcher.main import run_team_generation  # ✅ Import your core logic



# Create FastMCP instance
mcp = FastMCP("krivisio-tools", host="0.0.0.0", port=8000)


# ----------------------------- Project Estimation Tool -----------------------------

class ProjectEstimationInput(BaseModel):
    """
    Request model for the project estimation tool.

    Attributes:
        model_name (str): Name of the estimation model to run (e.g., "cocomo2").
        data (dict): Input parameters required for the selected model.
    """
    model_name: str = Field(..., description="Estimation model to run (e.g., cocomo2)")
    data: Dict[str, Any] = Field(..., description="Input data required by the model")


class ProjectEstimationOutput(BaseModel):
    """
    Response model for the project estimation tool.

    Attributes:
        model (str): The model that was executed.
        result (dict): The output produced by the model.
    """
    model: str
    result: Dict[str, Any]


@mcp.tool(description="Run a project estimation using algorithms like COCOMO II.")
def project_estimation(input_data: ProjectEstimationInput) -> ProjectEstimationOutput:
    """
    Execute the selected project estimation algorithm.

    Args:
        input_data (ProjectEstimationInput): Contains model name and input parameters.

    Returns:
        ProjectEstimationOutput: The result of running the selected estimation model.

    Raises:
        ValueError: If the model is unsupported or input is malformed.
        RuntimeError: For any internal errors during estimation.
    """
    try:
        result = run_estimation(input_data.model_name, input_data.data)
        return ProjectEstimationOutput(
            model=input_data.model_name.lower(),
            result=result
        )
    except ValueError as ve:
        raise ValueError(f"Input validation failed: {ve}")
    except Exception as e:
        raise RuntimeError(f"Estimation failed: {e}")


# ----------------------------- Report Generation Tool -----------------------------

class DocumentGenerationInput(BaseModel):
    """
    Request model for the report/document generation tool.

    Attributes:
        module (str): The module type (e.g., 'onboarding').
        doc_type (str): The specific document type (e.g., 'proposal').
        input_data (dict): The input data to render the template.
    """
    module: str = Field(..., description="Document module (e.g., 'onboarding')")
    doc_type: str = Field(..., description="Document type to generate (e.g., 'proposal')")
    input_data: Dict[str, Any] = Field(..., description="Input data for the selected document template")


class DocumentGenerationOutput(BaseModel):
    """
    Response model for the document generation tool.

    Attributes:
        document (str): The rendered document content.
    """
    document: str


@mcp.tool(description="Generate documents such as proposals using LLMs and pre-defined templates.")
def document_generation(input_data: DocumentGenerationInput) -> DocumentGenerationOutput:
    """
    Dispatch document generation using the report generation module.

    Args:
        input_data (DocumentGenerationInput): Template metadata and content input.

    Returns:
        DocumentGenerationOutput: Final document content string.

    Raises:
        ValueError: If the module or doc_type is unsupported.
        RuntimeError: If generation fails internally.
    """
    try:
        result = run_generation(
            module=input_data.module,
            doc_type=input_data.doc_type,
            input_data=input_data.input_data
        )
        return DocumentGenerationOutput(document=result)
    except ValueError as ve:
        raise ValueError(f"Invalid input: {ve}")
    except Exception as e:
        raise RuntimeError(f"Document generation failed: {e}")


# ----------------------------- Talent Matcher Tool -----------------------------

class TalentMatchInput(BaseModel):
    """
    Input model for Talent Matching Tool

    Attributes:
        specsheet (dict): Project specification input.
        candidates (list): List of available candidate profiles.
    """
    specsheet: Dict[str, Any] = Field(..., description="Project spec with requirements, e.g. tech stack, etc.")
    candidates: List[Dict[str, Any]] = Field(..., description="List of candidate dictionaries")


class TalentMatchOutput(BaseModel):
    """
    Output model for Talent Matching Tool

    Attributes:
        selected_team (list): Final selected team of candidates.
    """
    selected_team: List[Dict[str, Any]]


@mcp.tool(description="Run talent matching to assign the best-fit team based on tech stack and manager score.")
def match_talent(input_data: TalentMatchInput) -> TalentMatchOutput:
    """
    Match candidates to project requirements using talent matching logic.

    Args:
        input_data (TalentMatchInput): Contains specsheet and candidate pool.

    Returns:
        TalentMatchOutput: List of selected candidate dicts.
    """
    try:
        team = run_team_generation(spec_data=input_data.specsheet, candidate_pool=input_data.candidates)
        return TalentMatchOutput(
            selected_team=[member.dict() for member in team]
        )
    except Exception as e:
        raise RuntimeError(f"Talent matching failed: {e}")


# ----------------------------- Server Runner -----------------------------

if __name__ == "__main__":
    mcp.run(transport="sse")
