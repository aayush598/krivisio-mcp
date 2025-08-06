# core/constants.py

# Define the domains your tool supports for mapping
ALLOWED_DOMAINS = [
    "frontend", "backend", "devops", "ai/ml", "qa",
    "data engineering", "cloud engineering", "database administration",
    "ci/cd", "ux/ui"
]

# A strict mapping between various domain keywords to internal domains
DOMAIN_MAPPING = {
    # Frontend
    "frontend": "frontend",
    "ui": "frontend",
    "ux": "frontend",
    "client": "frontend",

    # Backend
    "backend": "backend",
    "api": "backend",
    "server": "backend",
    "database": "backend",
    "db": "backend",

    # DevOps
    "devops": "devops",
    "infrastructure": "devops",
    "deployment": "devops",
    "containerization": "devops",
    "containers": "devops",
    "orchestration": "devops",
    "ci/cd": "devops",
    "cicd": "devops",

    # AI/ML
    "ai/ml": "ai/ml",
    "ai": "ai/ml",
    "ml": "ai/ml",
    "machine_learning": "ai/ml",
    "artificial_intelligence": "ai/ml",
    "data_science": "ai/ml",

    # QA
    "qa": "qa",
    "testing": "qa",
    "quality_assurance": "qa",
}
