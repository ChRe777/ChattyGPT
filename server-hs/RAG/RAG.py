import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('..'))

from haystack_ import Document, Pipeline, ChatMessage, ChatPromptBuilder, OllamaChatGenerator
from haystack_ import InMemoryBM25Retriever, InMemoryDocumentStore


# Write documents to InMemoryDocumentStore
document_store = InMemoryDocumentStore()
document_store.write_documents([
    Document(content="My name is Jean and I live in Paris."),
    Document(content="My name is Mark and I live in Berlin."),
    Document(content="My name is Giorgio and I live in Rome.")
])

# Build a RAG pipeline
prompt_template = [
    ChatMessage.from_system("You are a helpful assistant."),
    ChatMessage.from_user(
        "Given these documents, answer the question.\n"
        "Documents:\n{% for doc in documents %}{{ doc.content }}{% endfor %}\n"
        "Question: {{question}}\n"
        "Answer:"
    )
]

# Define required variables explicitly
prompt_builder = ChatPromptBuilder(template=prompt_template, required_variables=["question", "documents"])

retriever = InMemoryBM25Retriever(document_store=document_store)
llm = OllamaChatGenerator(
    #model="deepseek-r1:1.5b",
    model="llama3.2",
    url = "http://localhost:11434",
    generation_kwargs={
        "num_predict": 100,
        "temperature": 0.2, # **
    }
)

rag_pipeline = Pipeline()
#
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
#
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm.messages")

#  query -> [retriver] -> documents
#  documents -> [prompt_builder]
#   question -> [prompt_builder] -> messages
#   messages -> [llm]

# Ask a question
question = "Who lives in Paris?"
results = rag_pipeline.run(
    {
        "retriever": {"query": question},
        "prompt_builder": {"question": question},
    }
)

lastMessage: ChatMessage = results["llm"]["replies"][-1]
print(lastMessage.text)

#rag_pipeline.draw(path="rag_pipeline.png")
#
print(rag_pipeline.dumps())

pipeline_dump = """
components:
  llm:
    init_parameters:
      generation_kwargs:
        num_predict: 100
        temperature: 0.2
      keep_alive: null
      model: llama3.2
      response_format: null
      streaming_callback: null
      timeout: 120
      tools: null
      url: http://localhost:11434
    type: haystack_integrations.components.generators.ollama.chat.chat_generator.OllamaChatGenerator
  prompt_builder:
    init_parameters:
      required_variables:
      - question
      - documents
      template:
      - content:
        - text: You are a helpful assistant.
        meta: {}
        name: null
        role: system
      - content:
        - text: 'Given these documents, answer the question.

            Documents:

            {% for doc in documents %}{{ doc.content }}{% endfor %}

            Question: {{question}}

            Answer:'
        meta: {}
        name: null
        role: user
      variables: null
    type: haystack.components.builders.chat_prompt_builder.ChatPromptBuilder
  retriever:
    init_parameters:
      document_store:
        init_parameters:
          bm25_algorithm: BM25L
          bm25_parameters: {}
          bm25_tokenization_regex: (?u)\b\w\w+\b
          embedding_similarity_function: dot_product
          index: 020e9007-04a1-4ced-b464-17d2df25e5ca
        type: haystack.document_stores.in_memory.document_store.InMemoryDocumentStore
      filter_policy: replace
      filters: null
      scale_score: false
      top_k: 10
    type: haystack.components.retrievers.in_memory.bm25_retriever.InMemoryBM25Retriever
connection_type_validation: true
connections:
- receiver: prompt_builder.documents
  sender: retriever.documents
- receiver: llm.messages
  sender: prompt_builder.prompt
max_runs_per_component: 100
metadata: {}
"""
