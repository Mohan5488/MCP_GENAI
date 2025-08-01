from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")# Basic Server Name

@mcp.tool()
def add(x, y):
    """Summary_
    Adds two numbers.
    """
    return int(x) + int(y)

@mcp.tool()
def subtract(x, y):
    """Summary_
    Subtracts two numbers.
    """
    return int(x) - int(y)

@mcp.tool()
def multiply(x, y):
    """Summary_
    Multiplies two numbers.
    """
    return int(x) * int(y)

if __name__ == "__main__":
    mcp.run(transport="stdio")
