"""
Performance and load testing
"""
import time
from fastapi.testclient import TestClient
from rag_backend.main import app

client = TestClient(app)

class TestPerformance:
    def test_response_time(self):
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        response_time = end_time - start_time
        assert response_time < 5.0
        assert response.status_code == 200 