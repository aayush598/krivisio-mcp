from typing import Dict, Any, List
from pydantic import BaseModel, Field, root_validator


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

    Accepts BOTH:
      1) Old format: {"function": "process_document", "data": {...}}
      2) New format (data-only): {"document_input": "...", "document_type": "...", "github_token": ...}

    In case (2), it is coerced to case (1) with function="process_document".
    """
    function: str = Field(
        "process_document",
        description="GitHub function to run: init_repo, create_branch, update_repo, or process_document."
    )
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters required by the selected GitHub function."
    )

    @root_validator(pre=True)
    def coerce_new_or_partial_formats(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        # If it's already old format, pass through.
        if "function" in values and "data" in values:
            return values

        # If it's partial old format (has data but no function), assume process_document.
        if "data" in values and "function" not in values:
            return {"function": "process_document", "data": values["data"]}

        # If it's the new data-only format (no 'function'/'data' keys), wrap it.
        if "function" not in values and "data" not in values:
            # Treat entire dict as the "data" payload.
            return {"function": "process_document", "data": values}

        # Fallback: leave as-is (Pydantic will validate)
        return values

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

class ProjectPipelineInput(BaseModel):
    tool: str = Field(..., description="Tool identifier, e.g. 'cocomo2_parameters'")
    project_description: str = Field(..., description="Brief description of the project")

    class DataModel(BaseModel):
        level: str = Field(..., description="Project complexity level (e.g. beginner, intermediate, advanced)")
        features: List[str] = Field(..., description="List of features for the project")
        tech_stacks: List[str] = Field(..., description="Technology stack used in the project")

    class PreferencesModel(BaseModel):
        include_docs: bool = False
        include_tests: bool = False
        include_docker: bool = False
        include_ci_cd: bool = False
        custom_folders: List[str] = []
        framework_specific: bool = False

    data: DataModel
    preferences: PreferencesModel

class ProjectPipelineWrapper(BaseModel):
    """Wrapper to match the JSON structure where everything is under 'input_data'"""
    input_data: ProjectPipelineInput
    
# ------------------ Output Model ------------------
class ProjectPipelineOutput(BaseModel):
    proposal_document: str = Field(..., description="Generated proposal document content")
    structure: Dict[str, Any]