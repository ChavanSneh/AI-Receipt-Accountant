import chromadb
import os

# Ensure the directory exists
VECTOR_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chroma_db")
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

# Create or get the collection
collection = client.get_or_create_collection(name="receipt_items")

def add_to_vector_store(item_id, text, metadata):
    """Stores a receipt item's text into ChromaDB."""
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[str(item_id)]
    )

def query_vector_store(query_text, n_results=3):
    """Searches for items semantically."""
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results