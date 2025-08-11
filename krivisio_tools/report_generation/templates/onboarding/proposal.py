"""
Template builder for the Proposal Specification Sheet used in the Onboarding Phase.

Generates a complete LLM prompt using project metadata and COCOMO-II estimation results.
Designed to support multiple templates via unified input schema.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel


class ProposalTemplateInput(BaseModel):
    """Unified input schema for proposal prompt generation."""
    project_description: str
    tech_stack: List[str]
    complexity_level: str
    features: List[str]
    cocomo_results: Dict


def build_proposal_spec_prompt(data: ProposalTemplateInput) -> str:
    """
    Generate a comprehensive prompt for LLM to create a project specification document.

    Args:
        data (ProposalTemplateInput): Structured input containing project metadata and COCOMO-II results.

    Returns:
        str: Formatted LLM prompt string in Markdown format.
    """

    # Extract relevant fields
    project_description = data["project_description"]
    tech_stack = data["tech_stack"]
    level = data["complexity_level"]
    features = data["features"]
    cocomo = data["cocomo_results"]["results"]

    # Extract COCOMO estimation details safely with defaults
    sloc = cocomo.get("function_points", {}).get("sloc", "N/A")
    esloc = cocomo.get("reuse", {}).get("esloc", "N/A")
    total_sloc = cocomo.get("revl", {}).get("sloc_after_revl", "N/A")

    effort = cocomo.get("effort_schedule", {})
    person_months = effort.get("person_months", "N/A")
    dev_time = effort.get("development_time_months", "N/A")
    avg_team_size = effort.get("avg_team_size", "N/A")

    # Format features
    formatted_features = "\n".join(f"- {f}" for f in features)

    # Compose LLM prompt
    prompt = f"""
                You are a senior technical project manager.

                Create a comprehensive **project specification document** in **Markdown** format
                for a software project of description : {project_description} with a **{level}** complexity level.

                ---

                ### 🧩 Project Features
                {formatted_features}

                ---

                ### 🛠️ Technology Stack
                - **Tech Stack**: {tech_stack}

                ---

                ### 📊 COCOMO-II Estimation Summary
                - Estimated SLOC: {sloc}
                - Equivalent SLOC (with reuse): {esloc}
                - Total SLOC (after REVL): {total_sloc}
                - Estimated Effort: {person_months} person-months
                - Development Time: {dev_time} months
                - Average Team Size: {avg_team_size} members

                ---

                ### 📝 Specification Document Requirements

                Structure the document with the following sections:

                1. **Executive Summary** – Overview and key insights  
                2. **Project Overview** – Purpose, background, and goals  
                3. **Functional Requirements** – Feature-level breakdown  
                4. **Non-Functional Requirements** – Performance, scalability, reliability  
                5. **Technical Architecture** – System diagrams, services, tech stack  
                6. **Development Estimation** – Breakdown using COCOMO-II data  
                7. **Risk Assessment** – Project risks and mitigation strategies  
                8. **Deliverables & Milestones** – Timelines and phases  
                9. **Acceptance Criteria** – Completion definition and quality benchmarks  
                10. **Resource Requirements** – Roles, team structure, external dependencies  

                Use a professional and formal tone suitable for stakeholders and clients.
                Format the Markdown cleanly for readability and clarity.
            """

    return prompt.strip()
