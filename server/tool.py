import json

TOOL_CALL_PROMPT_OLD = """
Du bist ein Assistent, der Werkzeuge aufruft. Wenn ein Nutzer dich etwas fragt, das ein Werkzeug benötigt,
gib nur JSON im folgenden Format zurück, ansonsten antworte auf die Frage:

{
    "type": "function_call",
    "name": "TOOL_NAME",
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
    "type": "function_call",
    "name": "get_weather",
    "parameters": "{\"location\":\"Berlin, Germany\"}"
}

Verwende die Tool-Antwort, um eine freundliche, informative und natürliche Antwort für den Nutzer zu formulieren.

"""

TOOL_CALL_PROMPT = """
Du bist ein Assistent, der bei Bedarf Werkzeuge verwendet. Wenn eine Nutzerfrage eindeutig nach externer Information verlangt (z. B. aktuelle Daten, Websuche oder Wetter), kannst du das passende Tool aufrufen. Ansonsten antworte direkt.

Verwende nur dann ein Tool, wenn es einen klaren Mehrwert für die Beantwortung der Frage bietet.

Wenn du ein Tool verwendest, gib ausschließlich folgendes JSON-Format zurück:

{
    "type": "function_call",
    "name": "TOOL_NAME",
    "parameters": {
        "param1": "value1",
        "param2": "value2"
    }
}

Tools:
- get_weather(location: string)
- search_web(query: string)

Beispiel:
Frage: "Wie ist das Wetter in Berlin?"
Antwort:
{
    "type": "function_call",
    "name": "get_weather",
    "parameters": {
        "location": "Berlin, Germany"
    }
}

Nach dem Tool-Aufruf kannst du die Antwort nutzen, um dem Nutzer eine freundliche, informative und natürliche Antwort zu geben.
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
    return f"Das Wetter in {location} ist sonnig mit 25°C."

def search_web(query):
    return f"The query {query} was searched in web."

# Registry of tools
REGISTERED_TOOLS = {
    'get_weather': get_weather,
    'search_web': search_web,
}

def call_tool(call_info):

    # Extract tool call info
    tool_name = call_info['name']
    params = call_info['parameters']

    # Call the function dynamically
    if tool_name in REGISTERED_TOOLS:
        fn = REGISTERED_TOOLS[tool_name]
        result = fn(**params)
        return result
    else:
        return ""
