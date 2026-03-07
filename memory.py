from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Initialize the "Brain"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Setup the "Vault" (Now with explicit persist_directory)
vector_db = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=embeddings
)

def store_in_memory(text_content, metadata):
    # Add text and ensure it is saved to disk immediately
    vector_db.add_texts(texts=[text_content], metadatas=[metadata])
    # Note: In newer Chroma versions, auto-persist is default, 
    # but explicit persistence ensures data integrity.
    print("Memory Saved!")

# 3. Search Function (Improved with confidence score)
def search_memory(query):
    # similarity_search_with_score helps you filter out bad matches
    results = vector_db.similarity_search_with_score(query, k=3)
    return results