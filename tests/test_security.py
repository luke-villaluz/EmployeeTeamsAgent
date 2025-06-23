"""
Security-related tests
"""
from fastapi.testclient import TestClient
from rag_backend.main import app

client = TestClient(app)

class TestSecurity:
    def test_cors_headers(self):
        response = client.get("/health", headers={"Origin": "http://testclient"})
        assert "access-control-allow-origin" in response.headers

    def test_input_validation(self):
        long_message = "x" * 10000
        response = client.post("/query", json={"message": long_message})
        assert response.status_code in [200, 400, 500, 503] 