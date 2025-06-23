from ragagent.load_excel import load_excel_data
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from pathlib import Path

# === Settings ===
EXCEL_PATH = Path("data/MasterEmployeeProfiles.xlsx") 
INDEX_PATH = Path("index/faiss_index")          # output location

def embed_and_store():
    print(f"Loading Excel: {EXCEL_PATH}")
    documents = load_excel_data(str(EXCEL_PATH))

    print(f"Embedding {len(documents)} documents using Ollama (phi3)...")
    embeddings = OllamaEmbeddings(model="phi3")

    vectorstore = FAISS.from_documents(documents, embeddings)

    print(f"Saving FAISS index to: {INDEX_PATH}")
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_PATH))

    print("Done. Vector index saved.")

if __name__ == "__main__":
    embed_and_store()
