from dataclasses import dataclass, field
from typing import List

@dataclass
class ProjectPreferences:
    """
    Data class to hold user preferences for directory structure generation.
    """
    include_docs: bool = True
    include_tests: bool = True
    include_docker: bool = False
    include_ci_cd: bool = False
    custom_folders: List[str] = field(default_factory=list)
    framework_specific: bool = True

    def to_dict(self) -> dict:
        """Convert preferences to dictionary format (optional utility)."""
        return {
            "include_docs": self.include_docs,
            "include_tests": self.include_tests,
            "include_docker": self.include_docker,
            "include_ci_cd": self.include_ci_cd,
            "custom_folders": self.custom_folders,
            "framework_specific": self.framework_specific,
        }
