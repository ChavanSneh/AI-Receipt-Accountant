from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Initialize the "Brain"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Setup the "Vault"
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def store_in_memory(text_content, metadata):
    vector_db.add_texts(texts=[text_content], metadatas=[metadata])
    print("Memory Saved!")