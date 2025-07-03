import sys
import os
from typing import List

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('../..'))

from haystack_ import ChatMessage, ChromaDocumentStore, ChromaQueryTextRetriever
from haystack_ import ChatPromptBuilder, OllamaChatGenerator
from haystack_ import print_streaming_chunk, Pipeline, Agent
from haystack_ import Document, DocumentJoiner
from haystack import component

@component
class WriteDocuments:
    """
    A component generating personal welcome message and making it upper case
    """

    def __init__(
        self,
        filepath: str = "chat_documents.txt"
    ):
        self.filepath = filepath

    @component.output_types(documents=List[Document])
    def run(self, query: str, documents:List[Document]):

        with open(self.filepath, "a") as file:

            file.write("-"*100 + "\n\n")
            file.write(f"Question: {query}\n")
            file.write("\n")
            for index, document in enumerate(documents):
                if not document.content is None:
                    file.write(f"Used doc {index}:\n")
                    file.write(f"Score: {document.score}\n")
                    file.write(document.content)
                    file.write("\n\n")
                    file.write(f"{document}")
            file.write("\n\n")


        return {"documents":documents}


@component
class FilterDocumentsByScore:
    """
    A component generating personal welcome message and making it upper case
    """

    def __init__(
        self,
        score: float = 0.99
    ):
        self.score = score

    @component.output_types(documents=List[Document])
    def run(self, documents:List[Document]):

        result = []
        for document in documents:
            print(document.meta["page_number"], document.score)
            if document.score is not None and document.score < self.score:
                result.append(document)

        return {"documents":result}


# -----------------------------------------------------------------------------

generator = OllamaChatGenerator(
    model="llama3.2",
    url = "http://localhost:11434",
    generation_kwargs={
        "num_predict": 512,  # prompt + generated tokens
        "temperature": 0.9,
        "num_ctx": 131072,
    }
)

# -----------------------------------------------------------------------------

# messages = [ChatMessage.from_system("\nYou are a helpful, respectful and honest assistant"),
# ChatMessage.from_user("What's Natural Language Processing?")]
# print(generato r.run(messages=messages))

# -----------------------------------------------------------------------------

prompt_template = [ChatMessage.from_user(

"""
Given the following information, answer the question in full sentences
If the given context is empty. Say you don't know.

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


# -----------------------------------------------------------------------------

from haystack_ import InMemoryDocumentStore, InMemoryBM25Retriever

# Create in-memory document store
in_document_store = InMemoryDocumentStore()
all_documents = document_store.filter_documents()
in_document_store.write_documents(all_documents)
bm25_retriever = InMemoryBM25Retriever(document_store=in_document_store)

# -----------------------------------------------------------------------------

joiner = DocumentJoiner(join_mode="reciprocal_rank_fusion", top_k=5)
prompt_builder = ChatPromptBuilder(template=prompt_template, required_variables=["question", "documents"])

agent = Agent(
    chat_generator=generator,
    streaming_callback=print_streaming_chunk,
)

writer = WriteDocuments()

#filter_score = FilterDocumentsByScore(score=1.2)

# see https://docs.haystack.deepset.ai/docs/automergingretriever
#
rag_pipeline = Pipeline()

rag_pipeline.add_component("chroma_retriever", chroma_retriever)
rag_pipeline.add_component("bm25_retriever", bm25_retriever)
rag_pipeline.add_component("joiner", joiner)

rag_pipeline.add_component("writer", writer)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("agent", agent)
#rag_pipeline.add_component("filter_score", filter_score)

rag_pipeline.connect("chroma_retriever", "joiner")
rag_pipeline.connect("bm25_retriever", "joiner")
rag_pipeline.connect("joiner.documents", "prompt_builder.documents")
rag_pipeline.connect("joiner.documents", "writer.documents")
rag_pipeline.connect("prompt_builder.prompt", "agent.messages")
#rag_pipeline.connect("filter_score.documents", "prompt_builder.documents")
#rag_pipeline.connect("filter_score.documents", "writer.documents")


def get_pages_by_book_id(documents):
    books = {}
    for doc in used_documents:
        book_id= doc.meta["book_id"]
        if not book_id in books:
            books[doc.meta["book_id"]] = set()
        books[doc.meta["book_id"]].add(doc.meta["page_number"])
    return books


def generate_further(pages, book):
    pages_sorted = sorted(pages)
    last_page = pages_sorted.pop()
    pages_str = ", ".join([str(page) for page in pages_sorted])
    return f"For further information, see pages {pages_str} and {last_page} in {book}."


# RUN IT ----
#

while True:
    user_input = input("\n> ")
    if user_input.lower() in ("/exit", "/quit"):
        break

    question = user_input
    result = rag_pipeline.run({
        "chroma_retriever": {"query": question},
        "bm25_retriever": {"query": question},
        "writer": {"query": question},
        "prompt_builder":   {"question": question},
    })

    used_documents = result["writer"]["documents"]
    pages_by_book = get_pages_by_book_id(used_documents)
    for book in pages_by_book:
        pages = pages_by_book[book]
        print("\n"+generate_further(pages, book))
