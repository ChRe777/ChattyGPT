# Haystack
#
from haystack import Pipeline
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder

# Create components
#
document_store = ChromaDocumentStore(persist_path="./chroma_db")
embedder = OllamaTextEmbedder(model="nomic-embed-text")
retriever = ChromaEmbeddingRetriever(document_store=document_store, top_k=2)

# Create pipeline
#
pipeline = Pipeline()
pipeline.add_component("embedder", embedder)
pipeline.add_component("retriever", retriever)
pipeline.connect("embedder.embedding", "retriever.query_embedding")

# Run
result = pipeline.run({"text":"first document"})
print(result["retriever"])

# Test
#
expected_result = """{
   "documents":[

      Document(id=0,
        "content":"This is the first document.",
        "meta":{
            "model":"nomic-embed-text",
            "created":"2025-06-26"
        },
        "score":49.71613311767578,
        "embedding":vector of size 768
      ),

      Document(
        id=1,
        "content":"This is the second document.",
        "meta":{
            "created":"2025-06-26",
            "model":"nomic-embed-text"
         },
        "score":300.430908203125,
        "embedding":vector of size 768
        )
   ]
}
"""
