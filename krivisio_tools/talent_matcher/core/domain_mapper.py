# core/domain_mapper.py

from typing import Dict, Set, Tuple
from krivisio_tools.talent_matcher.core.constants import DOMAIN_MAPPING, ALLOWED_DOMAINS


def map_tech_stack_to_candidate_domains(tech_stack: Dict[str, list]) -> Tuple[Dict[str, str], Set[str]]:
    """
    Map incoming tech stack domains to internal candidate domains.
    
    Returns:
        valid_domain_mapping: Mapping of tech domain → internal candidate domain
        requested_domains: Set of valid, deduplicated candidate domains requested
    """
    valid_domain_mapping = {}
    requested_candidate_domains = set()

    for tech_domain in tech_stack.keys():
        normalized = tech_domain.lower().replace(" ", "_").replace("-", "_")
        mapped_domain = DOMAIN_MAPPING.get(normalized)

        if mapped_domain and mapped_domain in ALLOWED_DOMAINS:
            valid_domain_mapping[tech_domain] = mapped_domain
            requested_candidate_domains.add(mapped_domain)
        else:
            print(f"[Domain Mapping Warning] Unrecognized or unsupported domain: '{tech_domain}'")

    return valid_domain_mapping, requested_candidate_domains
