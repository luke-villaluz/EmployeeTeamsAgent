"""
Configuration management for the RAG backend
"""
import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_title: str = "Employee Teams RAG API"
    api_version: str = "1.0.0"
    api_description: str = "Local RAG pipeline for employee data queries"
    
    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "phi3"
    ollama_embedding_model: str = "phi3"
    
    # FAISS Configuration
    faiss_index_path: str = "faiss_index"
    faiss_allow_dangerous_deserialization: bool = True
    
    # Data Configuration
    excel_data_path: str = "../data/employees.xlsx"
    
    # RAG Configuration
    rag_chain_type: str = "stuff"
    rag_k: int = 4  # Number of documents to retrieve
    rag_search_type: str = "similarity"
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # CORS Configuration
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    # Security Configuration
    enable_rate_limiting: bool = False
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour
    
    # Performance Configuration
    max_concurrent_requests: int = 10
    request_timeout: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

def get_excel_path() -> str:
    """Get the absolute path to the Excel file"""
    # If it's a relative path, make it absolute from the project root
    if not os.path.isabs(settings.excel_data_path):
        # Get the directory where this config file is located
        config_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up to the project root and then to the data directory
        project_root = os.path.dirname(config_dir)
        return os.path.join(project_root, settings.excel_data_path)
    return settings.excel_data_path

def get_faiss_index_path() -> str:
    """Get the absolute path to the FAISS index"""
    if not os.path.isabs(settings.faiss_index_path):
        config_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(config_dir, settings.faiss_index_path)
    return settings.faiss_index_path

def validate_configuration() -> bool:
    """Validate that all required configuration is present"""
    errors = []
    
    # Check if Excel file exists
    excel_path = get_excel_path()
    if not os.path.exists(excel_path):
        errors.append(f"Excel file not found: {excel_path}")
    
    # Check if FAISS index exists
    faiss_path = get_faiss_index_path()
    if not os.path.exists(faiss_path):
        errors.append(f"FAISS index not found: {faiss_path}")
    
    # Check Ollama connection
    try:
        import requests
        response = requests.get(f"{settings.ollama_base_url}/api/tags", timeout=5)
        if response.status_code != 200:
            errors.append(f"Ollama not accessible at {settings.ollama_base_url}")
    except Exception as e:
        errors.append(f"Cannot connect to Ollama: {e}")
    
    if errors:
        print("Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("Configuration validation passed!")
    return True

def print_configuration():
    """Print current configuration for debugging"""
    print("Current Configuration:")
    print(f"  API Title: {settings.api_title}")
    print(f"  API Version: {settings.api_version}")
    print(f"  Host: {settings.host}")
    print(f"  Port: {settings.port}")
    print(f"  Ollama URL: {settings.ollama_base_url}")
    print(f"  Ollama Model: {settings.ollama_model}")
    print(f"  Excel Path: {get_excel_path()}")
    print(f"  FAISS Index Path: {get_faiss_index_path()}")
    print(f"  RAG K: {settings.rag_k}")
    print(f"  Log Level: {settings.log_level}")

if __name__ == "__main__":
    print_configuration()
    validate_configuration() 