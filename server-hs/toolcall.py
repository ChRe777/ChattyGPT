import requests
import json

# Define the function/tool the assistant could call
def get_weather(location):
    return f"The weather in {location} is sunny and 25°C."

# Initial system prompt and user input
messages = [
    {"role": "system", "content": "You can call tools like get_weather. Respond in JSON if a tool should be used."},
    {"role": "user", "content": "What's the weather in Paris?"}
]


# Call Ollama's chat endpoint
response = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2",  # or whatever model you have
    "stream": False,
    "messages": messages,
    "stop": ["<|start_header_id|>", "<|end_header_id|>", "<|eot_id|>"]
})

print(response.content)
# Print assistant's raw response
assistant_response = response.json()["message"]["content"]
print("Assistant:", assistant_response)

# Try to parse as JSON (assuming the assistant responded with a tool call)
try:
    tool_call = json.loads(assistant_response)
    if tool_call.get("tool") == "get_weather":
        result = get_weather(tool_call.get("args", {}).get("location"))
        print("Tool output:", result)

        # Continue the conversation with tool result
        messages.append({"role": "assistant", "content": assistant_response})
        messages.append({"role": "function", "name": "get_weather", "content": result})

        follow_up = requests.post("http://localhost:11434/api/chat", json={
            "model": "llama3",
            "messages": messages
        })
        print("Assistant follow-up:", follow_up.json()["message"]["content"])

except json.JSONDecodeError:
    print("No tool call detected.")
