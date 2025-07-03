from haystack_ import Pipeline, ChatMessage,  OllamaChatGenerator, AnswerBuilder, AnswerJoiner




query = "What's Natural Language Processing?"
messages = [ChatMessage.from_system("You are a helpful, respectful and honest assistant. Be super concise."),
            ChatMessage.from_user(query)]

pipe = Pipeline()
pipe.add_component("llama", OllamaChatGenerator(model="llama3.2"))
pipe.add_component("deepseek", OllamaChatGenerator(model="deepseek-r1:1.5b"))
pipe.add_component("aba", AnswerBuilder())
pipe.add_component("abb", AnswerBuilder())
pipe.add_component("joiner", AnswerJoiner())

pipe.connect("llama.replies", "aba")
pipe.connect("deepseek.replies", "abb")
pipe.connect("aba.answers", "joiner")
pipe.connect("abb.answers", "joiner")

results = pipe.run(data={"llama": {"messages": messages},
                         "deepseek": {"messages": messages},
                         "aba": {"query": query},
                         "abb": {"query": query}})

print(results)
