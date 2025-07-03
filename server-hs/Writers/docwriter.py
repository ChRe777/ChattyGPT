import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('..'))

from haystack_ import Document, InMemoryDocumentStore, DocumentWriter, InMemoryBM25Retriever

documents = [
    Document(content="This is document 1", meta={"path":"/docs/file1.txt", "language":"en", "category":"news"}),
    Document(content="Das ist ein Document", meta={"path":"/docs/file2.txt", "language":"de"})
]

document_store = InMemoryDocumentStore()
writer = DocumentWriter(document_store = document_store)
result = writer.run(documents=documents)
print(result)
exprected_result = {'documents_written': 2}

result = document_store.bm25_retrieval(query = "document")
print(result)

print()

retriever = InMemoryBM25Retriever(document_store=document_store)

# see https://docs.haystack.deepset.ai/docs/metadata-filtering

filters={
    "field": "language",
    "operator": "==",
    "value": "de"
}

filters = {
    "operator": "AND",
    "conditions": [
        {"field": "language", "operator": "==", "value": "en"},
        {"field": "category", "operator": "in", "value": ["news", "blog"]},
        {
            "operator": "OR",
            "conditions": [
                {"field": "path", "operator": "==", "value": "/docs/file1.txt"},
                {"field": "path", "operator": "==", "value": "/docs/file2.txt"}
            ],
        }
    ]
}

result = retriever.run(query="document", filters=filters)
print(result)
