from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder

from haystack.dataclasses.chat_message import ChatMessage
from haystack.dataclasses.streaming_chunk import StreamingChunk

from haystack.components.builders.prompt_builder import PromptBuilder

from haystack import Pipeline
from typing import List

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
# print(generator.run(messages=messages))

# -----------------------------------------------------------------------------

template = """
Given the following information, answer the question.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{ query }}?
"""

# Create components
#
document_store = ChromaDocumentStore(persist_path="./chroma_db")
embedder = OllamaTextEmbedder(model="nomic-embed-text")
retriever = ChromaEmbeddingRetriever(document_store=document_store, top_k=2)
prompt_builder = PromptBuilder(template=template, required_variables=["query", "documents"])

# Pipeline
#
#
# query -> [embedder] -> embedding
# embedding -> [retriever] -> documents
# documents, query -> [prompt_builder] -> prompt
#
#
pipe = Pipeline()
#
pipe.add_component("embedder", embedder)
pipe.add_component("retriever", retriever)
pipe.add_component("prompt_builder", prompt_builder)
#
pipe.connect("embedder.embedding", "retriever.query_embedding")
pipe.connect("retriever.documents", "prompt_builder.documents")

query = "What is wrong with you?"

result = pipe.run(data={"prompt_builder": {"query": query}, "embedder": {"text": query}})
prompt = result["prompt_builder"]["prompt"]

# --------------------

messages = [
    ChatMessage.from_system("\nYou are a helpful, respectful and honest assistant"),
    ChatMessage.from_user(prompt)
]

from haystack.components.generators.utils import print_streaming_chunk
from haystack.components.agents.agent import Agent
from haystack.tools import Tool

def echo(query: str="foo") -> str:
    res = f"Tool executed with QUERY: {query}"
    return res

echo_tool = Tool(
    name="echo_tool",
    description="Echoes the query (demo tool).",
    function=echo,
    parameters={"query": {"type": "string", "description": "Search query"}},
)

agent = Agent(
    chat_generator=generator,
    tools=[echo_tool],
    system_prompt=(
        "Use tool to print the query to test tools. Do not answer the question, just send the query to the tool"
    ),
    max_agent_steps=5,
    raise_on_tool_invocation_failure=False,
    streaming_callback=print_streaming_chunk,
)

def chat(messages: List[ChatMessage], callback_fn):

    messages = [
        ChatMessage.from_system("\nYou are a helpful, respectful and honest assistant"),
        ChatMessage.from_user(prompt)
    ]

    def streaming_chunk(chunk: StreamingChunk) -> None:

        """StreamingChunk(content='',
            meta={'model': 'llama3.2',
                'created_at': '2025-06-26T18:14:11.944205Z',
                'done': True,
                'done_reason': 'stop',
                'total_duration': 5522938917,
                'load_duration': 23154375,
                'prompt_eval_count': 152,
                'prompt_eval_duration': 603993541,
                'eval_count': 54,
                'eval_duration': 4888944875,
                'role': 'assistant'
            }
        )
        """

        data = {}
        try:
            data = {
                "model": chunk.meta["model"],
                "created_at": chunk.meta["created_at"],
                "message": {"role": chunk.meta["role"], "content": chunk.content},
                "done_reason": chunk.meta["done_reason"],
                "done": chunk.meta["done"]
            }
        except:
            print("chunk - ", chunk)
            # chunk - StreamingChunk(content='', meta={'tool_result': 'Tool executed with QUERY: foo', 'tool_call': ToolCall(tool_name='echo_tool', arguments={}, id=None)})
            # chunk - StreamingChunk(content='', meta={'finish_reason': 'tool_call_results'})

        callback_fn(data)

    agent.run(messages=messages, streaming_callback=streaming_chunk)


def foo():

    result = agent.run(messages=messages)

    for message in result["messages"]:
        print("\n======")
        if message.role == "system":
            continue
        elif message.role == "tool":
            print(f"{message.role}:")
            print(f"Tool Results: {[tool.result for tool in message.tool_call_results]}")
            print(f"Used Tools: {[tool.origin.tool_name for tool in message.tool_call_results]}\n")
        else:
            print(f"{message.role}: {message.text}")
            print(f"Used Tools: {[tool.tool_name for tool in message.tool_calls]}\n")
