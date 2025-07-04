import ollama


def get_current_weather(location):
    return f"The weather in {location} is sunny with 25 degrees."


response = ollama.chat(
    model='llama3.2',
    stream=True,
    messages=[
        {'role': 'user', 'content':'Tell me the weather in Vienna?'},
    ],

	# provide a weather checking tool to the model
    tools=[{
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
        },
      },
    },
  ],
)

for x in response:
    if "message" in x:
        message = x["message"]
        if "tool_calls" in message:
             tools_calls = message["tool_calls"]
             for tools_call in tools_calls:
                 function = tools_call["function"]
                 function_name = function["name"]
                 function_args = function["arguments"]
                 function_result = globals()[function_name](**function_args)
                 print(function_result)

#print(response['message']['tool_calls'])
