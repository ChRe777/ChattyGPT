import ollama
import chromadb
import shortuuid

documents = [
  "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
  "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
  "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
  "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
  "Llamas are vegetarians and have very efficient digestive systems",
  "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="docs")
#collection = client.create_collection(name="docs")

# store each document in a vector embedding database
for i, doc in enumerate(documents):

  # Get embeddings - see https://ollama.com/blog/embedding-models
  response = ollama.embed(model="llama3.2", input=doc)
  embeddings = response["embeddings"]

  # Add to collection
  collection.add(
    ids=[str(i)],
    embeddings=embeddings,
    metadatas=[{"docId": shortuuid.uuid(), "path": f"/docs/{i}doc.txt"}],
    documents=[doc]
  )
