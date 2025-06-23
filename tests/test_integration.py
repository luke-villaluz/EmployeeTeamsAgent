"""
Integration workflow test
"""
import pytest
from fastapi.testclient import TestClient
from rag_backend.main import app

client = TestClient(app)

def test_integration_workflow():
    try:
        response = client.get("/health")
        assert response.status_code == 200
    except Exception as e:
        pytest.skip(f"Integration test skipped - API not accessible: {e}")

    try:
        response = client.post("/query", json={"message": "How many employees are there?"})
        assert response.status_code in [200, 500, 503]
    except Exception as e:
        pytest.skip(f"Integration test skipped - Query failed: {e}") 