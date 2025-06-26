# Haystack
#
from haystack import Document, component, Pipeline
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder

# Lib
#
import shortuuid
from typing import List


@component
class OllamaTextEmbeddings:
    """
    A component generating personal welcome message and making it upper case
    """

    def __init__(self, model="nomic-embed-text"):
        self.embedder = OllamaTextEmbedder(model=model)

    @component.output_types(embeddings=List[List[float]])
    def run(self, texts: List[str]) -> dict:
        embeddings = []
        for text in texts:
            result = self.embedder.run(text=text)
            embedding = result["embedding"]  # type: ignore[reportArgumentType]
            embeddings.append(embedding)

        return {"embeddings": embeddings}


@component
class ChromaDocumentStoreImporter:
    """
    A component generating personal welcome message and making it upper case
    """

    def __init__(self, document_store):
        self.document_store = document_store

    @component.output_types(ids=List[int])
    def run(self, embeddings: List[List[float]]) -> dict:
        docs = []
        ids = []
        for embedding in embeddings:
            id = shortuuid.uuid()
            doc = Document(
                id=id,  # 👈 Unique ID per document
                content="foo",
                embedding=embedding,  # type: ignore[reportArgumentType]
                meta={"foo": "bar"},  # type: ignore[reportArgumentType]
            )
            ids.append(id)
            docs.append(doc)
        self.document_store.write_documents(docs)
        return {"ids": ids}


# Init ChromaDB
#
# document_store = ChromaDocumentStore(persist_path="./chroma_db") # on disk

texts = ["This is the first document.", "This is the second document."]

document_store = ChromaDocumentStore()  # InMemory
embedder = OllamaTextEmbeddings(model="nomic-embed-text")
importer = ChromaDocumentStoreImporter(document_store=document_store)

pipeline = Pipeline()

pipeline.add_component("embedder", embedder)
pipeline.add_component("importer", importer)
pipeline.connect("embedder.embeddings", "importer.embeddings")

result = pipeline.run(data={"texts": texts})

print(result)
print(document_store.count_documents())
