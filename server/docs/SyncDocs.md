Perfect — you're using **Chroma** (Chromadb), so here’s exactly how you update your documents when they've changed.

---

## ✅ Steps to Update Documents in **Chroma (chromadb)**

### 🔁 1. **Identify the changed document**

Use a unique `id` per document or chunk. If your source changes, find the affected IDs.

---

### 🧽 2. **Delete the old vectors**

You can delete by `ids`:

```python
collection.delete(ids=["doc123"])
```

Or by `where` metadata filter:

```python
collection.delete(where={"source": "myfile.md"})
```

---

### 🧠 3. **Re-embed the updated document**

Use your embedding model (e.g. OpenAI, HuggingFace) to get the new embedding for the updated content:

```python
from openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings().embed(["Updated document content"])
```

---

### 📥 4. **Add (or upsert) new data**

Use `add()` if you just deleted the old version:

```python
collection.add(
    ids=["doc123"],
    documents=["Updated document content"],
    embeddings=[embeddings],
    metadatas=[{"source": "myfile.md", "updated_at": "2025-06-25"}]
)
```

Or use `upsert()` (available in newer versions of Chroma):

```python
collection.upsert(
    ids=["doc123"],
    documents=["Updated document content"],
    embeddings=[embeddings],
    metadatas=[{"source": "myfile.md"}]
)
```

> `upsert` = update if exists, insert if not — very handy for sync logic.

---

## 🛠️ Bonus: Automate updates

You could write a sync function like this:

```python
def sync_document(doc_id, new_text, metadata):
    collection.delete(ids=[doc_id])
    new_embedding = embed(new_text)
    collection.add(
        ids=[doc_id],
        documents=[new_text],
        embeddings=[new_embedding],
        metadatas=[metadata]
    )
```

---

## ✅ Summary for Chroma

| Step          | Code                                              |
| ------------- | ------------------------------------------------- |
| Delete old    | `collection.delete(ids=[...])`                    |
| Re-embed      | `embedding_model.embed([...])`                    |
| Add or Upsert | `collection.add(...)` or `collection.upsert(...)` |

---

Let me know if you're chunking documents or want a complete "sync all changed docs" script — happy to build that too.
