from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("FunAPIs")

@mcp.tool()
def get_cat_fact() -> str:
    """Get a random cat fact."""
    return requests.get("https://catfact.ninja/fact").json()["fact"]

@mcp.tool()
def get_advice() -> str:
    """Get a random piece of advice."""
    return requests.get("https://api.adviceslip.com/advice").json()["slip"]["advice"]

@mcp.tool()
def get_activity_suggestion() -> dict:
    """Get a suggested activity for boredom."""
    return requests.get("https://www.boredapi.com/api/activity").json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
