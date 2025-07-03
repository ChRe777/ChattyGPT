import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('../..'))

# HierarchicalDocumentSplitter works together with
#
# See https://docs.haystack.deepset.ai/docs/automergingretriever
#
# Use AutoMergingRetriever to improve search results by returning complete parent documents
# instead of fragmented chunks when multiple related pieces match a query.

from haystack_ import DocumentWriter, DocumentCleaner
from haystack_ import HierarchicalDocumentSplitter
from haystack_ import ChromaDocumentStore




# pip install pypdf
# see https://docs.haystack.deepset.ai/docs/pypdftodocument
#
from datetime import datetime
from haystack.components.converters.pypdf import PyPDFToDocument
converter = PyPDFToDocument()
results = converter.run(sources=["fia_2026_formula_1_technical_regulations_issue_8_-_2024-06-24_SMALL.pdf"], meta={"date_added": datetime.now().isoformat()})
documents = results["documents"]

cleaner = DocumentCleaner()
result = cleaner.run(documents)
documents = result["documents"]

text = documents[-1].content
word_count = len(text.split())

print("Word count:", word_count) # 92692 words


# [Document(id=cf8bcf8b618000ac6756c7b361958f24f6d78c4550fc2198be585248dae78de6, content: '2026 Formula 1 Technical Regulations 1 24 June 2024
# © 2024 Fédération Internationale de l’Automobil...', meta: {'file_path': 'fia_2026_formula_1_technical_regulations_issue_8_-_2024-06-24.pdf', 'date_added': '2025-06-30T16:53:26.865464'})]

# chunk 200-300 words
# overlap 50 words
#
# [             full text           ]
# [           ]
#          [             ]
#                     [             ]

# 92692/12000 = 8

splitter = HierarchicalDocumentSplitter(block_sizes={1000, 333}, split_overlap=50, split_by="word")
result = splitter.run(documents)
documents = result["documents"]


#
import json
def clean_metadata(meta: dict) -> dict:
    """
    Prepares metadata for Chroma by:
    - Keeping only JSON-serializable types.
    - Serializing lists and dicts as JSON strings.
    """
    cleaned = {}
    for k, v in meta.items():
        if isinstance(v, (str, int, float, bool)): # Supported by ChromaDb
            cleaned[k] = v
        elif isinstance(v, (list, dict)): # NOT Supported by ChromaDb
            cleaned[k] = json.dumps(v)  # Serialize complex types
        # Other types (e.g., custom objects) are ignored
    return cleaned

def fix_unsupported_meta(documents):
    for document in documents:
        document.meta = clean_metadata(document.meta)


# Init ChromaDB
#
# document_store = ChromaDocumentStore(persist_path="./chroma_db") # on disk
document_store = ChromaDocumentStore(
    persist_path="./chroma_db",
    embedding_function="OllamaEmbeddingFunction", # does http://localhost:17.../api/embe...
    model_name="nomic-embed-text:latest"
)  # InMemory

# Model	                    Context Window	Languages	    Embedding Size	Notes
# nomic-embed-text:latest	2K tokens	    English only	 768 dims	     Good default
# To fully utilize the 2K token context window without overflow, chunk size should be around 1,300 to 1,400 words.
# Keep some margin for safety (e.g., 1,200 words) to avoid cutting off or errors.
# Overlapping chunks (e.g., 100-200 words overlap) can help maintain context continuity.

fix_unsupported_meta(documents)

#print(documents[-1])

writer = DocumentWriter(document_store = document_store)
result = writer.run(documents=documents)

print(document_store.count_documents())

# Document 0f096faac57c729d84e43c0dde394c2d6233fe6e7b8db3230aec48fe71e4c4c5 contains
# `meta` values of unsupported types for the keys: __children_ids, _split_overlap.
# These items will be discarded. Supported types are: str, int, float, bool.

#pipeline = Pipeline()
#pipeline.add_component("converter", PyPDFToDocument())
#pipeline.add_component("cleaner", DocumentCleaner())
#pipeline.add_component("splitter", DocumentSplitter(split_by="sentence", split_length=5))
#pipeline.add_component("writer", DocumentWriter(document_store=document_store))
