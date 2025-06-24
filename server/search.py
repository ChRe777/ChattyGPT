import ollama
import chromadb

def getDocs(query):

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="docs")

    response = ollama.embed(model="llama3.2", input=query)
    embeddings = response["embeddings"]
    result = collection.query(
        query_embeddings=embeddings,
        n_results=3,
    )

    if result is not None and result["documents"]:
        return result["documents"][0]
    else:
        return []


if __name__ == '__main__':
    query = "How much weight can a llama carry relative to its body weight?"
    print(getDocs(query))

test = """
    Answer query from given context and only from this context:

    Query: How much weight can a llama carry relative to its body weight?
    Context:
    'Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall', 'Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight', "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels"
"""
