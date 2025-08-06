# core/candidate_selector.py

import math
import re
import json

from typing import List, Dict, Set
from krivisio_tools.talent_matcher.config import OPENAI_API_KEY, DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS
from krivisio_tools.talent_matcher.models.schema import CandidateOutput
from krivisio_tools.talent_matcher.utils.llm_client import chat_with_llm


def extract_available_candidates_by_domain(candidates: List[Dict], requested_domains: Set[str]) -> Dict[str, List[Dict]]:
    """Filter candidates that are available and in requested domains"""
    available = {}
    for c in candidates:
        if c["availability"] and c["domain"] in requested_domains:
            available.setdefault(c["domain"], []).append(c)
    return available


def create_team_selection_prompt(
    tech_stack: Dict[str, List[str]],
    avg_team_size: float,
    manager_score_threshold: float,
    available_by_domain: Dict[str, List[Dict]],
    domain_mapping: Dict[str, str]
) -> str:
    """Constructs a system/user prompt for OpenAI to generate the team"""
    candidates_context = ""
    for domain, candidates in available_by_domain.items():
        candidates_context += f"\n{domain.upper()} DOMAIN:\n"
        for c in candidates:
            candidates_context += f"  - {c['name']}: Skills={c['skills']}, Manager Score={c['manager_score']}\n"

    tech_requirements = ""
    for tech_domain, techs in tech_stack.items():
        mapped = domain_mapping.get(tech_domain, "UNMAPPED")
        tech_requirements += f"  - {tech_domain} (maps to: {mapped}): {techs}\n"

    prompt = f"""
You are a STRICT domain-first candidate selector.

PROJECT REQUIREMENTS:
{tech_requirements}

AVAILABLE CANDIDATES BY DOMAIN:
{candidates_context}

RULES:
- ONLY select candidates from requested domains
- DO NOT substitute missing domains
- Manager score must be >= {manager_score_threshold} (preferably)
- Max team size: {math.ceil(avg_team_size)}

OUTPUT (raw JSON only):
{{
  "team_selection": [
    {{
            "name": "candidate_name",
            "domain": "candidate_domain",
            "skills": ["skill1", "skill2"],
            "manager_score": 4.5,
            "selection_reason": "Domain: [domain] | Manager Score: [score] >= {manager_score_threshold} | Tech Match: [matched_techs]",
            "tech_stack_match": ["matched_tech1", "matched_tech2"],
            "requested_for_domain": "original_tech_stack_domain"
        }}
  ]
}}
"""
    return prompt


def generate_team_selection(
    candidates: List[Dict],
    tech_stack: Dict[str, List[str]],
    avg_team_size: float,
    manager_score_threshold: float,
    domain_mapping: Dict[str, str],
    requested_domains: Set[str]
) -> List[CandidateOutput]:
    """Main function to generate a team selection"""
    max_team_size = math.ceil(avg_team_size)
    available_by_domain = extract_available_candidates_by_domain(candidates, requested_domains)
    prompt = create_team_selection_prompt(tech_stack, avg_team_size, manager_score_threshold, available_by_domain, domain_mapping)

    try:
        
        raw = chat_with_llm(prompt)
        cleaned = re.sub(r"```(?:json)?", "", raw).strip("`\n ")
        parsed = json.loads(cleaned)
        team = parsed.get("team_selection", [])

    except Exception as e:
        print(f"[OpenAI fallback]: {e}")
        team = []

    final_team = []
    used = set()

    # Validate and limit selection
    for selection in team:
        name = selection.get("name")
        domain = selection.get("domain")
        for c in candidates:
            if (
                c["name"] == name and
                c["domain"] == domain and
                c["availability"] and
                name not in used and
                domain in requested_domains
            ):
                final_team.append(CandidateOutput(
                    name=c["name"],
                    domain=c["domain"],
                    skills=c["skills"],
                    manager_score=c["manager_score"]
                ))
                used.add(name)
                break

        if len(final_team) >= max_team_size:
            break

    return final_team
