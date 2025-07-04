from haystack_ import OllamaChatGenerator
from haystack_ import Agent
from haystack_ import ChatMessage

# see https://ollama.com/blog/tool-support


# 1. Define your tool
def multiply_numbers(a: int, b: int) -> int:
    return a * b

from haystack.tools import Tool

_parameters = {
    "type": "object",
    "properties": {
        "a": {"type": "integer"},
        "b": {"type": "integer"}
    },
    "required": ["a", "b"]
}

"""
'type': 'function',
'function': {
  'name': 'get_current_weather',
  'description': 'Get the current weather for a location',
  'parameters': {
    'type': 'object',
    'properties': {
      'location': {
        'type': 'string',
        'description': 'The name of the location',
      },
    },
    'required': ['location'],
"""

tool = Tool(
    name="multiply_numbers",
    description="Multiplies two integers.",
    function=multiply_numbers,
    parameters={"a": int, "b": int}
)


# 2. Define your LLaMA-style prompt template

system_prompt="""<|start_header_id|>system<|end_header_id|>
Cutting Knowledge Date: December 2023
You are a helpful assistant with tool calling capabilities.
<|eot_id|>
{% for message in chat_history %}
<|start_header_id|>{{ message.role }}<|end_header_id|>
{{ message.content }}
<|eot_id|>
{% endfor %}
<|start_header_id|>assistant<|end_header_id|>"""


system_prompt="""Cutting Knowledge Date: December 2023
You are a helpful assistant with tool calling capabilities.
"""

prompt = """
<|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023

{{ if .System }}{{ .System }}
{{- end }}
{{- if .Tools }}When you receive a tool call response, use the output to format an answer to the orginal user question.

You are a helpful assistant with tool calling capabilities.
{{- end }}<|eot_id|>
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 }}
{{- if eq .Role "user" }}<|start_header_id|>user<|end_header_id|>
{{- if and $.Tools $last }}

Given the following functions, please respond with a JSON for a function call with its proper arguments that best answers the given prompt.

Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}. Do not use variables.

{{ range $.Tools }}
{{- . }}
{{ end }}
{{ .Content }}<|eot_id|>
{{- else }}

{{ .Content }}<|eot_id|>
{{- end }}{{ if $last }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- else if eq .Role "assistant" }}<|start_header_id|>assistant<|end_header_id|>
{{- if .ToolCalls }}
{{ range .ToolCalls }}
{"name": "{{ .Function.Name }}", "parameters": {{ .Function.Arguments }}}{{ end }}
{{- else }}

{{ .Content }}
{{- end }}{{ if not $last }}<|eot_id|>{{ end }}
{{- else if eq .Role "tool" }}<|start_header_id|>ipython<|end_header_id|>

{{ .Content }}<|eot_id|>{{ if $last }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- end }}
{{- end }}
"""

example = """
<|start_header_id|>system<|end_header_id|>
You are a helpful assistant.
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
What's the capital of France?
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
The capital of France is Paris.
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
And what's the population?
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
As of 2023, Paris has a population of around 2.1 million people.
<|eot_id|>
"""

from typing import List, Dict, Any

def render_chat(system: str = "", tools: List[str] = None, messages: List[Dict[str, Any]] = None):
    output = ""

    # System message section
    output += "<|start_header_id|>system<|end_header_id|>\n\n"
    output += "Cutting Knowledge Date: December 2023\n\n"
    if system:
        output += f"{system}\n"
    if tools:
        output += "When you receive a tool call response, use the output to format an answer to the orginal user question.\n\n"
        output += "You are a helpful assistant with tool calling capabilities.\n"
    output += "<|eot_id|>\n"

    # Iterate through messages
    for i, msg in enumerate(messages or []):
        last = (i == len(messages) - 1)
        role = msg.get("Role")
        content = msg.get("Content", "")
        tool_calls = msg.get("ToolCalls", [])

        if role == "user":
            output += "<|start_header_id|>user<|end_header_id|>\n"
            if tools and last:
                output += "\nGiven the following functions, please respond with a JSON for a function call with its proper arguments that best answers the given prompt.\n\n"
                output += 'Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}. Do not use variables.\n\n'
                for tool in tools:
                    output += f"{tool}\n"
            output += f"{content}<|eot_id|>\n"
            if last:
                output += "<|start_header_id|>assistant<|end_header_id|>\n"

        elif role == "assistant":
            output += "<|start_header_id|>assistant<|end_header_id|>\n"
            if tool_calls:
                for call in tool_calls:
                    name = call["Function"]["Name"]
                    args = call["Function"]["Arguments"]
                    output += f'{{"name": "{name}", "parameters": {args}}}'
            else:
                output += f"{content}"
            if not last:
                output += "<|eot_id|>"

        elif role == "tool":
            output += "<|start_header_id|>ipython<|end_header_id|>\n\n"
            output += f"{content}<|eot_id|>"
            if last:
                output += "<|start_header_id|>assistant<|end_header_id|>\n"

    return output

# 3. Create the OllamaGenerator with llama3
generator = OllamaChatGenerator(
    model="llama3.2",  # or llama3:latest if you've pulled a specific tag
    url = "http://localhost:11434",
    generation_kwargs={
        "num_predict": 100,
        "temperature": 0.9,
    }
)


# 4. Setup the agent with your tool and generator
agent = Agent(
    chat_generator=generator,
    tools=[tool],
    system_prompt=system_prompt
)


# 5. Simulate a user chat message
chat_messages = [
    ChatMessage.from_user("What's 12 times 7?")
]

# 6. Run the agent
response = agent.run(chat_messages)

# 7. Show the response
print("🔁 Agent Final Response:")
print(response["last_message"].text)
