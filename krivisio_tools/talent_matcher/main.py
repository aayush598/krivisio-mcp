# main.py

from krivisio_tools.talent_matcher.core.requirements_extractor import extract_requirements_from_spec
from krivisio_tools.talent_matcher.core.domain_mapper import map_tech_stack_to_candidate_domains
from krivisio_tools.talent_matcher.core.candidate_selector import generate_team_selection
from krivisio_tools.talent_matcher.models.schema import SpecInput, CandidateOutput
from typing import List
import sys
import json


def run_team_generation(spec_data: dict, candidate_pool: List[dict]) -> List[CandidateOutput]:
    # Step 1: Extract requirements from the spec
    requirements = extract_requirements_from_spec(spec_data)
    tech_stack = requirements.get("tech_stack", {})
    avg_team_size = requirements.get("avg_team_size", 3.0)
    manager_score_threshold = requirements.get("manager_score_threshold", 4.0)

    # Step 2: Map domains
    domain_mapping, requested_domains = map_tech_stack_to_candidate_domains(tech_stack)

    if not requested_domains:
        print("[ERROR] No valid domains were found in the tech stack.")
        return []

    # Step 3: Generate team
    final_team = generate_team_selection(
        candidates=candidate_pool,
        tech_stack=tech_stack,
        avg_team_size=avg_team_size,
        manager_score_threshold=manager_score_threshold,
        domain_mapping=domain_mapping,
        requested_domains=requested_domains
    )

    return final_team


# === Optional CLI Usage ===
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <spec.json> <candidates.json>")
        sys.exit(1)

    spec_file = sys.argv[1]
    candidates_file = sys.argv[2]

    with open(spec_file, "r") as f:
        spec_data = json.load(f)

    with open(candidates_file, "r") as f:
        candidate_pool = json.load(f)

    team = run_team_generation(spec_data, candidate_pool)
    print("\n=== Final Team Selection ===")
    for member in team:
        print(member.json(indent=2))
