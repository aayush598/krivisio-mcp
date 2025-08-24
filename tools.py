from krivisio_tools.github.main import handle_github_action
from krivisio_tools.side_tools.main import run_tool
from krivisio_tools.project_evaluation.main import run_estimation
from krivisio_tools.report_generation.app.main import run_generation
from krivisio_tools.project_structure_generator.core.agent import run_structure_generation_agent
from krivisio_tools.project_structure_generator.models.preferences import ProjectPreferences


from models import GitHubToolInput, GitHubToolOutput, ProjectPipelineWrapper, ProjectPipelineInput, ProjectPipelineOutput
from typing import Union, Dict, Any

import json


from dotenv import load_dotenv
import os


load_dotenv()


from logger import get_logger
log = get_logger(__name__)


def tool1(input_data: Union[GitHubToolInput, Dict[str, Any]]) -> GitHubToolOutput:
    log.info("Starting GitHub action handler", extra={"extra_data": {"tool": "tool1"}})
    try:
        # Normalize any incoming format to the canonical (old) format via the model
        normalized = GitHubToolInput.parse_obj(input_data)

        # Create the exact old-format payload expected downstream
        old_format_payload: Dict[str, Any] = {
            "function": normalized.function,
            "data": normalized.data,
        }

        result = handle_github_action(old_format_payload)
        result = result["classified_features"]

        print("="*100)
        print(result)
        print("="*100)

        log.info("GitHub action completed successfully", extra={"extra_data": {"tool": "tool1"}})
        return result
    except Exception as e:
        log.exception(f"GitHub action failed with error : {e}", extra={"extra_data": {"tool": "tool1"}})
        raise


def tool2(input_data: ProjectPipelineWrapper) -> ProjectPipelineOutput:

   project_description = input_data.pop("project_description")
   preferences = input_data.pop("preferences")
   input_data = input_data


   cocomo_parameters = run_tool(input_data)


   project_evaluation_data = run_estimation(model_name="cocomo2", data=cocomo_parameters)


   proposal_input = {
       "project_description": project_description,
       "tech_stack": input_data["data"]["tech_stacks"],
       "complexity_level" : input_data["data"]["level"],
       "features" : input_data["data"]["features"],
       "cocomo_results" : project_evaluation_data,
   }
   proposal_document = run_generation(
           module="onboarding",
           doc_type="proposal",
           input_data=proposal_input
       )


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
           input_data["data"]["features"],
           input_data["data"]["tech_stacks"],
           preferences
       )


   return {"proposal_document":proposal_document,
           "folder_structure":structure}


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

