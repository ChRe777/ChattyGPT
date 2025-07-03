from haystack_ import ChatMessage, Agent, OllamaChatGenerator

# Step 1: Define your generator (LLM backend)
generator = OllamaChatGenerator(model="llama3.2")

# Step 2: Create the agent with memory
agent = Agent(
    chat_generator=generator,
    name="Assistant", components=[generator], memory=[])  # memory is a list of ChatMessages

# Step 3: Simulate a conversation
def ask(question: str):
    reply = agent.run(question)
    print("Assistant:", reply["replies"][0])

# Example chat
ask("Who is Albert Einstein?")
ask("Where was he born?")
ask("What was his contribution to physics?")
