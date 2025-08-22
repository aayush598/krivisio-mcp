from krivisio_tools.github.main import handle_github_action
from krivisio_tools.side_tools.main import run_tool
from krivisio_tools.project_evaluation.main import run_estimation
from krivisio_tools.report_generation.app.main import run_generation

from models import GitHubToolInput, GitHubToolOutput

from dotenv import load_dotenv
import os

load_dotenv()

def tool1(input_data: GitHubToolInput) -> GitHubToolOutput:
    return handle_github_action(input_data)

def tool2(input_data: dict) -> dict:
    project_description = input_data.pop("project_description")
    input_data = input_data

    cocomo_parameters = run_tool(input_data)
    print("="*40)
    print(f"cocomo_parameters : {cocomo_parameters}")

    project_evaluation_data = run_estimation(model_name="cocomo2", data=cocomo_parameters)
    print("="*40)
    print(f"project_evaluation_data : {project_evaluation_data}")

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
    
    print("="*40)
    print(f"proposal_document : {proposal_document}")

    return run_tool(input_data)

if __name__ == "__main__":
    # Example usage
    input_data = {
        "tool": "cocomo2_parameters",
        "data": {
            "level": "intermediate",
            "features": ["Login", "Shopping cart", "Payment gateway", "AI recommendations"],
            "tech_stacks": ["Python", "Django", "React"]
        },
        "project_description" : "Chatbot project for customer service"
        }
    output = tool2(input_data)