import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('../..'))

from haystack_ import ChatMessage, ChromaDocumentStore, ChromaQueryTextRetriever
from haystack_ import ChatPromptBuilder, OllamaChatGenerator
from haystack_ import Agent, AutoMergingRetriever, AnswerBuilder
from haystack_ import print_streaming_chunk, Pipeline

# -----------------------------------------------------------------------------

generator = OllamaChatGenerator(
    model="llama3.2",
    url = "http://localhost:11434",
    generation_kwargs={
        "num_predict": 100,
        "temperature": 0.9,
    }
)

# -----------------------------------------------------------------------------

# messages = [ChatMessage.from_system("\nYou are a helpful, respectful and honest assistant"),
# ChatMessage.from_user("What's Natural Language Processing?")]
# print(generato r.run(messages=messages))

# -----------------------------------------------------------------------------

prompt_template = [ChatMessage.from_user(

"""
Given the following information, answer the question.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{ question }}?
"""

)]


# Create components
#
document_store = ChromaDocumentStore(
    persist_path="./chroma_db",
    embedding_function="OllamaEmbeddingFunction", # does http://localhost:17.../api/embe...
    model_name="nomic-embed-text:latest"
)

chroma_retriever = ChromaQueryTextRetriever(document_store=document_store, top_k=5)
auto_merging = AutoMergingRetriever(document_store=document_store, threshold=0.6)
prompt_builder = ChatPromptBuilder(template=prompt_template, required_variables=["question", "documents"])

agent = Agent(
    chat_generator=generator,
    max_agent_steps=5,
    streaming_callback=print_streaming_chunk,
)


# see https://docs.haystack.deepset.ai/docs/automergingretriever
#
rag_pipeline = Pipeline()
rag_pipeline.add_component("chroma_retriever", chroma_retriever)
rag_pipeline.add_component("auto_retriever", auto_merging)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("agent", agent)
rag_pipeline.add_component("answer_builder", AnswerBuilder())

rag_pipeline.connect("chroma_retriever.documents", "auto_retriever.documents")
rag_pipeline.connect("auto_retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder.prompt", "agent.messages")
rag_pipeline.connect("agent.messages", "answer_builder.replies")
rag_pipeline.connect("chroma_retriever", "answer_builder.documents")


# RUN IT ----
#

while True:
    user_input = input("\n> ")
    if user_input.lower() in ("/exit", "/quit"):
        break

    question = user_input
    result = rag_pipeline.run({
        "chroma_retriever": {"query": question},
        "prompt_builder":   {"question": question},
        "answer_builder":   {"query": question}
    })

    #print(result['agent']['last_message'].text)
