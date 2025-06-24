import ollama
import chromadb

def getDocs(query):

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="docs")

    response = ollama.embed(model="llama3.2", input=query)
    embeddings = response["embeddings"]
    query_result = collection.query(
        query_embeddings=embeddings,
        n_results=3,
    )

    example = """
    {
        'ids': [['2', '1', '4']],
        'embeddings': None,
        'documents': [['Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall', 'Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands', 'Llamas are vegetarians and have very efficient digestive systems']],
        'uris': None,
        'included': ['metadatas', 'documents', 'distances'],
        'data': None,
        'metadatas': [[None, None, None]],
        'distances': [[1.294952392578125, 1.3026795387268066, 1.3163938522338867]]
    }
    """

    if query_result is None:
        return []

    THRESHOLD = 1.0

    results = zip(
        query_result['ids'][0],
        query_result['documents'][0],
        query_result['distances'][0]
    )

    filtered = [
        {'id': _id, 'doc': doc, 'distance': dist}
        for _id, doc, dist in results
        if dist < THRESHOLD
    ]

    return filtered


if __name__ == '__main__':
    query = "How much weight can a llama carry relative to its body weight?"
    print(getDocs(query))

test = """
    Answer query from given context and only from this context:

    Query: How much weight can a llama carry relative to its body weight?
    Context:
    'Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall', 'Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight', "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels"
"""
