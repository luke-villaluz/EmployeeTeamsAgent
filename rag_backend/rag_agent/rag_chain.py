# src/ragagent/rag_chain.py

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

def build_rag_chain():
    # Load vectorstore
    vectorstore = FAISS.load_local("rag_backend/faiss_index", embeddings=OllamaEmbeddings(model="phi3"), allow_dangerous_deserialization=True)

    # Initialize retriever
    retriever = vectorstore.as_retriever()

    # Local LLM (phi3 via Ollama)
    llm = Ollama(model="phi3")

    # Create RAG chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return rag_chain
