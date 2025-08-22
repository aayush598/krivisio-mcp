from krivisio_tools.github.main import handle_github_action
from krivisio_tools.side_tools.main import run_tool
from krivisio_tools.project_evaluation.main import run_estimation
from krivisio_tools.report_generation.app.main import run_generation
from krivisio_tools.project_structure_generator.core.agent import run_structure_generation_agent
from krivisio_tools.project_structure_generator.models.preferences import ProjectPreferences

from models import GitHubToolInput, GitHubToolOutput, ProjectPipelineWrapper, ProjectPipelineInput, ProjectPipelineOutput

import json

from dotenv import load_dotenv
import os

load_dotenv()

def tool1(input_data: GitHubToolInput) -> GitHubToolOutput:
    return handle_github_action(input_data)

def tool2(input_data: ProjectPipelineWrapper) -> ProjectPipelineOutput:
    # Get the inner model
    inner: ProjectPipelineInput = input_data.input_data

    # JSON string (Pydantic v2)
    input_json = inner.model_dump_json(indent=2)

    input_json = json.loads(input_json)

    project_description = input_json.pop("project_description")
    preferences = input_json.pop("preferences")
    input_json = input_json

    cocomo_parameters = run_tool(input_json)
    print("="*40)
    print(f"cocomo_parameters : {cocomo_parameters}")

    project_evaluation_data = run_estimation(model_name="cocomo2", data=cocomo_parameters)
    print("="*40)
    print(f"project_evaluation_data : {project_evaluation_data}")

    proposal_input = {
        "project_description": project_description,
        "tech_stack": input_json["data"]["tech_stacks"],
        "complexity_level" : input_json["data"]["level"],
        "features" : input_json["data"]["features"],
        "cocomo_results" : project_evaluation_data,
    }
    proposal_document = run_generation(
            module="onboarding",
            doc_type="proposal",
            input_data=proposal_input
        )
    
    print("="*40)
    print(f"proposal_document : {proposal_document}")

    preferences = ProjectPreferences(
        include_docs=preferences.get("include_docs", False),
        include_tests=preferences.get("include_tests", False),
        include_docker=preferences.get("include_docker", False),
        include_ci_cd=preferences.get("include_ci_cd", False),
        custom_folders=preferences.get("custom_folders", []),
        framework_specific=preferences.get("framework_specific", False),
    )
    structure = run_structure_generation_agent(
            project_description,
            input_json["data"]["features"],
            input_json["data"]["tech_stacks"],
            preferences
        )
    
    print("="*40)
    print(f"proposal_document : {structure}")

    return {"proposal_document":proposal_document,
            "structure":structure}

if __name__ == "__main__":
    # Example usage
    input_data = {
        "tool": "cocomo2_parameters",
        "data": {
            "level": "intermediate",
            "features": ["Login", "Shopping cart", "Payment gateway", "AI recommendations"],
            "tech_stacks": ["Python", "Django", "React"]
        },
        "project_description" : "Chatbot project for customer service",
        "preferences" : {
            "include_docs": False,
            "include_tests": False,
            "include_docker": False,
            "include_ci_cd": False,
            "custom_folders": ["assets", "utils"],
            "framework_specific": False
        }
        }
    output = tool2(input_data)