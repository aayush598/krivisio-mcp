# models/schema.py

from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class TechStack(BaseModel):
    """Represents the extracted tech stack by domain."""
    tech_stack: Dict[str, List[str]]
    avg_team_size: float
    manager_score_threshold: float


class CandidateOutput(BaseModel):
    """Output structure for a selected candidate."""
    name: str
    domain: str
    skills: List[str]
    manager_score: float


class TeamSelection(BaseModel):
    """Structure of the full team output."""
    team_selection: List[CandidateOutput]
    selection_summary: Optional[Dict] = None


class SpecInput(BaseModel):
    """Input spec (used when not parsing file directly)."""
    specsheet: Dict
