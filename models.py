from typing import Dict, Any, List
from pydantic import BaseModel, Field


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

# ----------------------------- Folder Structure Generation Tool -----------------------------

class StructureGenerationInput(BaseModel):
    """
    Input model for folder structure generation tool.
    
    Attributes:
        description (str): Short project description.
        tech_stack (list): List of technologies used.
        preferences (dict): Structure preferences.
    """
    description: str = Field(..., description="Brief project description.")
    features: List[str] = Field(..., description="List of project features.")
    tech_stack: List[str] = Field(..., description="List of technologies, e.g., ['react', 'node']")
    preferences: Dict[str, Any] = Field(..., description="Folder structure preferences")


class StructureGenerationOutput(BaseModel):
    """
    Output model for folder structure generation tool.

    Attributes:
        structure (dict): Generated folder structure tree.
    """
    structure: Dict[str, Any]

# ----------------------------- GitHub Tool -----------------------------

class GitHubToolInput(BaseModel):
    """
    Input model for GitHub Tool

    Attributes:
        function (str): The action to perform (init_repo, create_branch, update_repo).
        data (dict): The input data required for that function.
    """
    function: str = Field(..., description="GitHub function to run: init_repo, create_branch, or update_repo.")
    data: Dict[str, Any] = Field(..., description="Parameters required by the selected GitHub function.")


class GitHubToolOutput(BaseModel):
    """
    Output model for GitHub Tool

    Attributes:
        result (Any): The result from the GitHub action.
    """
    result: Any


# ----------------------------- Side Tools -----------------------------

class SideToolInput(BaseModel):
    """
    Generic input model for running any side_tool.

    Attributes:
        tool (str): Name of the tool to run (must exist in side_tools TOOLS dict).
        data (dict): Parameters required by the selected tool.
    """
    tool: str = Field(..., description="Tool name to run (as defined in side_tools TOOLS dict).")
    data: Dict[str, Any] = Field(..., description="Input parameters for the selected tool.")


class SideToolOutput(BaseModel):
    """
    Output model for side_tools execution.

    Attributes:
        result (Any): Output from the tool.
    """
    result: Any
