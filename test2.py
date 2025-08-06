from mcp import ClientSession
from mcp.client.sse import sse_client

# Example test input for onboarding_proposal tool
input_data = {
    "input_data": {
        "template_name": "proposal",
        "data": {
            "project_name": "SmartEdu LMS",
            "complexity_level": "Intermediate",
            "features": [
                "User authentication and role management",
                "Interactive course modules with quizzes",
                "Progress tracking and analytics",
                "Live video conferencing integration",
                "Admin dashboard for content management"
            ],
            "cocomo_results": {
                "results": {
                    "function_points": {
                        "sloc": 18000
                    },
                    "reuse": {
                        "esloc": 14500
                    },
                    "revl": {
                        "sloc_after_revl": 16000
                    },
                    "effort_schedule": {
                        "person_months": 24.5,
                        "development_time_months": 5.5,
                        "avg_team_size": 4.45
                    }
                }
            }
        }
    }
}


async def run():
    async with sse_client(url="http://0.0.0.0:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"Available tools: {tools}")

            # Call the second tool, i.e., onboarding_proposal
            result = await session.call_tool("document_generation", arguments=input_data)
            print("\n=== Tool Output ===")
            print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
