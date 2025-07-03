import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('../..'))

from haystack_ import RecursiveDocumentSplitter, DocumentSplitter, Document, DocumentCleaner
from haystack_ import ChromaDocumentStore, DocumentWriter

f = open("wu1_pages.txt")
content = f.read()

pages = {}
page_nr = 0
page_buffer = []

def onEndPage(page_nr, buffer):
    pages[page_nr] = "\n".join(buffer)

for line in content.splitlines():
    page_nr = 0
    page_buffer.append(line)
    try:
        page_nr = int(line.strip())
        page_buffer.pop()
        onEndPage(page_nr, page_buffer)
        page_buffer = [] # Reset Buffer
    except:
        page_nr = page_nr


def splitting_by_chapter(text):
    parts = text.split("\nChapter ")
    return parts[1:]

splitter = DocumentSplitter(
    split_by="function",
    splitting_function = splitting_by_chapter)

documents = [Document(content=content)]
result = splitter.run(documents=documents)

for document in result["documents"]:
    if not document.content is None:
        lines = document.content.splitlines()

        # Extract Chapter info
        chapter_number = lines[0]
        chapter_name = lines[1]

        document.meta["chapter_number"] = chapter_number
        document.meta["chapter_name"] = chapter_name

        # Remove first line
        document.content = "\n".join(lines[1:])

chunker = RecursiveDocumentSplitter(split_length=260, split_overlap=0, separators=["sentence"])
chunker.warm_up()
result = chunker.run(documents=result["documents"])

cleaner = DocumentCleaner()
result = cleaner.run(documents=result["documents"])
documents = result["documents"]

for document in documents:
    document.meta.pop("_split_overlap")

document_store = ChromaDocumentStore(
    persist_path="./chroma_db",
    embedding_function="OllamaEmbeddingFunction", # does http://localhost:17.../api/embe...
    model_name="nomic-embed-text:latest"
)  # InMemory

writer = DocumentWriter(document_store=document_store)
result = writer.run(documents=documents)

print(result)
