from tools import tool1, tool2
from typing import Dict
import json
from mcp.server.fastmcp import FastMCP
from models import ProjectPipelineWrapper, ProjectPipelineOutput


from logger import setup_logging, shutdown_logging, get_logger


# Logging setup
setup_logging(static_fields={"app":"my_service","env":"dev"})
log = get_logger(__name__)
log.info("App started")


# Create FastMCP instance
mcp = FastMCP("krivisio-tools", host="0.0.0.0", port=8000)




# ------------------ Tool 1: Feature suggestions ------------------
@mcp.tool(description="Automate GitHub tasks: init repo, branch, update repo.")
def generate_project_features(input_data: Dict) -> Dict:
   return tool1(input_data)


# ------------------ Tool 2: Project Estimation + Proposal + Structure ------------------
@mcp.tool(description="Run project evaluation pipeline: cocomo params, estimation, proposal, folder structure.")
def generate_project_proposal(input_data: Dict) -> Dict:
   output = tool2(input_data)
   return output


# ----------------------------- Server Runner -----------------------------


if __name__ == "__main__":
   mcp.run(transport="sse")


