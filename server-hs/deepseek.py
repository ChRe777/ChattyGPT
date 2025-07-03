from haystack_ import Agent, OllamaChatGenerator, ChatMessage
from haystack.components.generators.utils import print_streaming_chunk

generator = OllamaChatGenerator(
    model="deepseek-r1:1.5b",
    url = "http://localhost:11434",
    generation_kwargs={
        "num_predict": 100,
        "temperature": 0.9,
    }
)

agent = Agent(
    chat_generator=generator,
    streaming_callback=print_streaming_chunk,
)

while True:
    user_input = input("\n> ")
    if user_input.lower() in ("exit", "quit"):
        break

    user_message = ChatMessage.from_user(user_input)
    result = agent.run(messages=[user_message])
    #print(result["messages"][-1].text)
