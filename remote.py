import os
from fastmcp import FastMCP

mcp=FastMCP(name="calculator server")


@mcp.tool
def add_numbers(a:int,b:int)->int:
    """Adding two numbers"""
    return a+b

@mcp.tool
def subtract_numbers(a:int,b:int)->int:
    """Subtract two numbers"""
    return a-b

@mcp.tool
def multiply_numbers(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b

@mcp.tool
def divide_numbers(a:int,b:int)->int:
    """Divide two numbers"""
    return a/b


if __name__=="__main__":
    mcp.run(transport="streamable-http",host="0.0.0.0",port=8000)

