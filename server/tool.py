import json

TOOL_CALL_PROMPT = """
Du bist ein Assistent, der Werkzeuge aufruft. Wenn ein Nutzer dich etwas fragt, das ein Werkzeug benötigt, gib nur JSON im folgenden Format zurück:

{
    "tool": "TOOLNAME",
    "parameters": {
        "param1": "value1",
        "param2": "value2"
    }
}

Verwende keine erklärenden Texte außerhalb des JSON.

Tools:
- get_weather(location: string)
- search_web(query: string)

Beispiel:
Frage: "Wie ist das Wetter in Berlin?"
Antwort:
{
    "tool": "get_weather",
    "parameters": {
    "location": "Berlin"
    }
}

Wenn kein Werkzeug gefunden wird, antworte ganz normal auf die Frage.

"""

def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

def parse_tool_call(text):
    try:
        return json.loads(text)
    except:
        return None


def get_weather(location):
    return f"The weather in {location} is sunny and 25°C."

def search_web(query):
    return f"The query {query} was searched in web."

# Registry of tools
REGISTERED_TOOLS = {
    'get_weather': get_weather,
    'search_web': search_web,
}

def call_tool(call_info):

    # Extract tool call info
    tool_name = call_info['tool']
    params = call_info['parameters']

    # Call the function dynamically
    if tool_name in REGISTERED_TOOLS:
        fn = REGISTERED_TOOLS[tool_name]
        result = fn(**params)
        return result
    else:
        return ""
