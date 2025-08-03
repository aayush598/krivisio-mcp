from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.server.fastmcp import tools

async def run():
    async with sse_client(url="http://0.0.0.0:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"tools output : {tools}")

            result = await session.call_tool("add", arguments={"a": 4, "b": 5})
            print(f"result output : {result}")
            
            
if __name__ == "__main__":
    import asyncio
    asyncio.run(run())  