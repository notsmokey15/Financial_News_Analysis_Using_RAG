import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="../db")
collection = client.get_or_create_collection(name="financial_news")

def add_documents_to_db(documents: list[str], metadatas: list[dict]):
    """Embeds documents and adds them to the ChromaDB collection."""
    print(f"Embedding and adding {len(documents)} documents to the database...")
    embeddings = embedding_model.encode(documents).tolist()
    ids = [f"doc_{collection.count() + i}" for i in range(len(documents))] # Generates new unique IDs
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print("Documents added successfully.")

def query_documents(query: str, n_results: int = 5) -> list[str]:
    """Queries the collection for the most relevant document chunks."""
    print(f"Querying for: '{query}'...")
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results['documents'][0]
