# see https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/#json-based-tool-calling
#

from ollama import ChatResponse, chat, Message
from typing import Final
import json

MODEL: Final = "llama3.2"
# MODEL = 'tinyllama'
# see https://ollama.com/library/tinyllama
# see https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v0.6
# see https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct

# messages = [
#  {"role": "system", "content": "You are a bot that responds to weather queries."},
#  {"role": "user", "content": "Hey, what's the temperature in Paris right now?"}
# ]

# tool_call = {"name": "get_current_temperature", "arguments": {"location": "Paris, France"}}
# messages.append({"role": "assistant", "tool_calls": [{"type": "function", "function": tool_call}]})
# messages.append({"role": "tool", "name": "get_current_temperature", "content": "22.0"})


def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
        a (int): The first number
        b (int): The second number

    Returns:
        int: The sum of the two numbers
    """

    # The cast is necessary as returned tool call arguments don't always conform exactly to schema
    # E.g. this would prevent "what is 30 + 12" to produce '3012' instead of 42
    return int(a) + int(b)


def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers
    """

    # The cast is necessary as returned tool call arguments don't always conform exactly to schema
    return int(a) - int(b)


def get_weather(location: str) -> str:
    """
    Get weather of location
    """

    # return f"The weather in {location} is nice and sunny by 20°"
    return json.dumps(
        {
            "Location": "Berlin",
            "Temperature": "24°C",
            "Precipitation": "7%",
            "Humidity": "39%",
            "Wind": "11 km/h",
            "Description": "In Berlin zeigt sich morgens die Sonne zwischen einzelnen Wolken und die Temperatur liegt bei 24°C. Im weiteren Tagesverlauf gibt es überwiegend blauen Himmel,",
        }
    )
    # return "The weather in Berlin is sunny with 24° temperature"


# Tools can still be manually defined and passed into chat
subtract_two_numbers_tool = {
    "type": "function",
    "function": {
        "name": "subtract_two_numbers",
        "description": "Subtract two numbers",
        "parameters": {
            "type": "object",
            "required": ["a", "b"],
            "properties": {
                "a": {"type": "integer", "description": "The first number"},
                "b": {"type": "integer", "description": "The second number"},
            },
        },
    },
}

add_two_numbers_tool = {
    "type": "function",
    "function": {
        "name": "add_two_numbers",
        "description": "Add two numbers",
        "parameters": {
            "type": "object",
            "required": ["a", "b"],
            "properties": {
                "a": {"type": "integer", "description": "The first number"},
                "b": {"type": "integer", "description": "The second number"},
            },
        },
    },
}

get_weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather from location",
        "parameters": {
            "type": "object",
            "required": ["location"],
            "properties": {
                "location": {"type": "string", "description": "The location"}
            },
        },
    },
}

available_functions = {
    "add_two_numbers": add_two_numbers,
    "subtract_two_numbers": subtract_two_numbers,
    "get_weather": get_weather,
}

# ------------------------
#

query = "What is three minus one? And how is the weather in Berlin?"
messages = [Message(role="user", content=query)]

response: ChatResponse = chat(
    model=MODEL,
    messages=messages,
    tools=[add_two_numbers_tool, subtract_two_numbers_tool, get_weather_tool],
)

tool_results = []

if response.message.tool_calls:
    # There may be multiple tool calls in the response
    for tool in response.message.tool_calls:
        # Ensure the function is available, and then call it
        if function_to_call := available_functions.get(tool.function.name):
            print("Calling function:", tool.function.name)
            print("Arguments:", tool.function.arguments)
            output = function_to_call(**tool.function.arguments)
            tool_results.append({"output": output, "name": tool.function.name})
            print("Function output:", output)
        else:
            print("Function", tool.function.name, "not found")

# Only needed to chat with the model using the tool call results
if response.message.tool_calls:
    # Add the function response to messages for the model to use

    for tool_result in tool_results:

        m = Message(
            role="tool",
            content=str(tool_result["output"]),
        )
        messages.append(m)

    # Get final response from model with function outputs
    final_response = chat(
        model=MODEL,
        messages=messages,
        tools=[add_two_numbers_tool, subtract_two_numbers_tool, get_weather_tool],
    )
    print(final_response.message.content)

else:
    print("No tool calls returned from model")
