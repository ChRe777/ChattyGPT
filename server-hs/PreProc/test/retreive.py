import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('../..'))

from haystack_ import ChromaDocumentStore, ChromaQueryTextRetriever

document_store = ChromaDocumentStore(
    persist_path="./chroma_db",
    embedding_function="OllamaEmbeddingFunction", # does http://localhost:17.../api/embe...
    model_name="nomic-embed-text:latest"
)

chroma_retriever = ChromaQueryTextRetriever(document_store=document_store, top_k=5)
result = chroma_retriever.run(query="Energy Recovery System")
print(result["documents"][-1])

Document(
    id=a19b41b18919da0b2eabe2fe2b6e1def52b843ae91f33b355c312c6e763d7969,
    content: 'classification of the car’s components in terms of their Design, Intellectual Property, Manufacture ...',
    meta: {
       "page_number":3,
       "file_path":"fia_2026_formula_1_technical_regulations_issue_8_-_2024-06-24_SMALL.pdf",
       "_split_overlap":"[{\"doc_id\": \"29a6dbee08c84f95c7692c7b3d6574c4571f3531edf1e9015e3f55d296ad2d6e\", \"range\": [1801, 2128]}, {\"doc_id\": \"bdc545a3f08f131163852630c3008c997c69ac3acbb7d88606855988ef78369e\", \"range\": [0, 292]}]",
       "date_added":"2025-07-01T13:37:53.294564",
       "source_id":"ba135cd5213ac46e453a4b8ebe37de14853398788f1ccbeb269ee47b53dc8c5f",
       "split_id":2,
        "split_idx_start":3515,
       "__block_size":333,
       "__children_ids":"[]",
       "__level":2,
       "__parent_id":"ba135cd5213ac46e453a4b8ebe37de14853398788f1ccbeb269ee47b53dc8c5f"
    },
    score: 1.125553846359253,
    embedding: vector of size 768)
