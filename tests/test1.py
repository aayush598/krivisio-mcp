from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.server.fastmcp import tools

input_data = {
  "model_name": "cocomo2",
  "data": {
    "function_points": {
      "fp_items": [
        {"fp_type": "EI", "det": 8, "ftr_or_ret": 1},
        {"fp_type": "EO", "det": 10, "ftr_or_ret": 2},
        {"fp_type": "ILF", "det": 18, "ftr_or_ret": 3}
      ],
      "language": "Java"
    },
    "reuse": {
      "asloc": 3500,
      "dm": 20,
      "cm": 10,
      "im": 10,
      "su_rating": "L",
      "aa_rating": "2",
      "unfm_rating": "CF",
      "at": 15
    },
    "revl": {
      "new_sloc": 8500,
      "adapted_esloc": 2500,
      "revl_percent": 25
    },
    "effort_schedule": {
      "sloc_ksloc": 7.5,
      "sced_rating": "L"
    }
  }
}

async def run():
    async with sse_client(url="http://0.0.0.0:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"tools output : {tools}")

            result = await session.call_tool("project_estimation", arguments={"input_data": input_data})
            print(f"result output : {result}")
            
            
if __name__ == "__main__":
    import asyncio
    asyncio.run(run()) 