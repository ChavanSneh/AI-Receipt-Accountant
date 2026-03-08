from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize the embedding function once
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Dedicated collection for System Logic
vector_db = Chroma(persist_directory="./system_knowledge_db", embedding_function=embeddings)

def update_system_logic(logic_description):
    """Stores how the system should handle expenses."""
    vector_db.add_texts(texts=[logic_description], metadatas=[{"type": "rule"}])
    print("System rule updated in vault.")

def get_system_rules(query):
    """Retrieves specific operational logic."""
    results = vector_db.similarity_search(query, k=1)
    return results[0].page_content if results else "No specific rule found."