from krivisio_tools.project_structure_generator.models.preferences import ProjectPreferences
from krivisio_tools.project_structure_generator.core.agent import run_structure_generation_agent

desc = "Chatbot."
features = ["user authentication", "real-time messaging", "file sharing"]
tech = ["html", "css", "javascript"]
prefs = ProjectPreferences(include_docs=True, include_docker=True)

structure = run_structure_generation_agent(project_description=desc,features=features, tech_stack = tech, preferences=prefs)


print(f"structure: {structure}")