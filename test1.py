from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.server.fastmcp import tools

input_data =  {
        "tool": "cocomo2_parameters",
        "data": {
            "level": "intermediate",
            "features": ["Login", "Shopping cart", "Payment gateway", "AI recommendations"],
            "tech_stacks": ["Python", "Django", "React"]
        },
        "project_description" : "Chatbot project for customer service",
        "preferences" : {
            "include_docs": False,
            "include_tests": False,
            "include_docker": False,
            "include_ci_cd": False,
            "custom_folders": ["assets", "utils"],
            "framework_specific": False
        }
        }
async def run():
    async with sse_client(url="http://0.0.0.0:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"tools output : {tools}")

            result = await session.call_tool("proposal_generation", arguments={"input_data": input_data})
            print(f"result output : {result}")
            
            
if __name__ == "__main__":
    import asyncio
    asyncio.run(run()) 