f = open("./data/docs_with_pages.txt")
content = f.read()

import json
def parse_meta(line):
    meta = json.loads(line)
    return meta

docs = []

for line in content.splitlines():
    if line.startswith("---"):
        docs.append({
            "content": ""
        })
    elif line.startswith("{"):
        meta = parse_meta(line)
        meta.pop('split_id')
        meta.pop('split_idx_start')
        meta.pop('source_id')
        meta["book_id"] = "WU1"
        docs[-1]["meta"] = meta
    else:
        docs[-1]["content"] += line +"\n"


import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('../..'))

from haystack_ import Document
from typing import List

documents: List[Document] = []
for doc in docs:
    documents.append(Document(content=doc["content"], meta=doc["meta"]))

from haystack_ import ChromaDocumentStore, DocumentWriter
document_store = ChromaDocumentStore(
    persist_path="./chroma_db",
    embedding_function="OllamaEmbeddingFunction", # does http://localhost:17.../api/embe...
    model_name="nomic-embed-text:latest"
)  # InMemory

writer = DocumentWriter(document_store=document_store)
result = writer.run(documents=documents)

print(result)
