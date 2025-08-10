# krivisio_tools/side_tools/main.py

from krivisio_tools.side_tools.utils.cocomo2_parameters_generation import generate_cocomo2_parameters

TOOLS = {
    "cocomo2_parameters": generate_cocomo2_parameters
}

def run_tool(input_data: dict):
    """
    Run a registered tool with given input.

    Expected format:
    {
        "tool": "<tool_name>",
        "data": { ... parameters for that tool ... }
    }
    """
    tool_name = input_data.get("tool")
    if tool_name not in TOOLS:
        raise ValueError(f"Tool '{tool_name}' not found.")
    
    return TOOLS[tool_name](**input_data.get("data", {}))


# Example direct run
if __name__ == "__main__":
    test_input = {
        "tool": "cocomo2_parameters",
        "data": {
            "project_idea": "E-commerce site with AI recommendations",
            "level": "intermediate",
            "features": ["Login", "Shopping cart", "Payment gateway", "AI recommendations"],
            "tech_stacks": ["Python", "Django", "React"]
        }
    }
    result = run_tool(test_input)
    print(result)
