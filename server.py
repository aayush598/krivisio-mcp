from tools import tool1

from models import (
    ProjectEstimationInput, ProjectEstimationOutput,
    DocumentGenerationInput, DocumentGenerationOutput,
    TalentMatchInput, TalentMatchOutput,
    StructureGenerationInput, StructureGenerationOutput,
    GitHubToolInput, GitHubToolOutput,
    SideToolInput, SideToolOutput
)

from mcp.server.fastmcp import FastMCP

# Create FastMCP instance
mcp = FastMCP("krivisio-tools", host="0.0.0.0", port=8000)


# ------------------ Tool 1: Feature suggestions ------------------
@mcp.tool(description="Automate GitHub tasks: init repo, branch, update repo.")
def feature_generation(input_data):
    return tool1(input_data)



# ----------------------------- Server Runner -----------------------------

if __name__ == "__main__":
    mcp.run(transport="sse")
