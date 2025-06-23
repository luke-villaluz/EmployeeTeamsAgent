"""
Test cases for RAG backend endpoints
"""
from fastapi.testclient import TestClient
from rag_backend.main import app

client = TestClient(app)

class TestRAGBackend:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_api_info_endpoint(self):
        response = client.get("/api")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Employee Teams RAG API"
        assert "endpoints" in data

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "ollama_available" in data
        assert "faiss_index_loaded" in data

    def test_stats_endpoint(self):
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_query_endpoint_empty_message(self):
        response = client.post("/query", json={"message": ""})
        assert response.status_code in [400, 503]
        data = response.json()
        assert "detail" in data

    def test_query_endpoint_valid_message(self):
        response = client.post("/query", json={"message": "Who is the CTO?"})
        assert response.status_code in [200, 500, 503]
        if response.status_code == 200:
            data = response.json()
            assert "response" in data

    def test_query_endpoint_with_sources(self):
        response = client.post("/query", json={
            "message": "Who is the CTO?",
            "include_sources": True
        })
        assert response.status_code in [200, 500, 503]
        if response.status_code == 200:
            data = response.json()
            assert "response" in data
            assert "sources" in data 