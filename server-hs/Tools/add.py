def _add(a: int, b: int) -> int:
    return a + b

_parameters = {
    "type": "object",
    "properties": {
        "a": {"type": "integer"},
        "b": {"type": "integer"}
    },
    "required": ["a", "b"]
}

# -----------------------------------------------------------------------------

from haystack.tools import Tool

add_tool = Tool(name="addition_tool",
            description="This tool adds two numbers",
            parameters=_parameters,
            function=_add)

__all__ = ['add_tool']


# print(add_tool.tool_spec)
# print(add_tool.invoke(a=15, b=10))
