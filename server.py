#!/usr/bin/env python3
"""
MCP Integration for Project Estimation Tool

Registers the project estimation engine as a tool within the MCP server.
Supports dynamic algorithm dispatch such as COCOMO II and more.

Author: Aayush Gid
"""

from typing import Dict, Any

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from krivisio_tools.project_evaluation.main import run_estimation

# Create FastMCP instance
mcp = FastMCP("project-evaluation", host="0.0.0.0", port=8000)


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


if __name__ == "__main__":
    mcp.run(transport="sse")
