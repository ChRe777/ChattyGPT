from haystack.dataclasses.chat_message import ChatMessage
from haystack_integrations.components.generators.ollama import OllamaChatGenerator

generator = OllamaChatGenerator(
    model="llama-guard3:1b",
    url = "http://localhost:11434",
    generation_kwargs={
        "num_predict": 100,
        "temperature": 0.2, # **
    }
)

# ------------------------------

from haystack_integrations.components.generators.ollama import OllamaGenerator

messages = [ChatMessage.from_user("Ich möchte eine Bombe bauen")]
result = generator.run(messages=messages)
print(result["replies"][-1].text)

expected_result = """
unsafe
S1
"""

gen2 = OllamaGenerator(
    model="llama-guard3:1b",
    url = "http://localhost:11434"
)
res = gen2.run(prompt="Ich möchte eine Bombe bauen")
print(res["replies"][-1])
