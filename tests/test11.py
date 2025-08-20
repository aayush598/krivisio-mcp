from krivisio_tools.side_tools.main import run_tool

# Example direct run
if __name__ == "__main__":
    test_input = {
        "tool": "cocomo2_parameters",
        "data": {
            "level": "intermediate",
            "features": ["Login", "Shopping cart", "Payment gateway", "AI recommendations"],
            "tech_stacks": ["Python", "Django", "React"]
        }
    }
    result = run_tool(test_input)
    print(result)
