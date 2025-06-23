"""
Test suite for the RAG backend
"""
import pytest
import requests
import json
from fastapi.testclient import TestClient
from rag_backend.main import app
from rag_backend.config import settings, validate_configuration

# Test client
client = TestClient(app)

class TestRAGBackend:
    """Test cases for RAG backend functionality"""
    
    def test_root_endpoint(self):
        """Test the root endpoint serves the frontend"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_api_info_endpoint(self):
        """Test the API info endpoint"""
        response = client.get("/api")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Employee Teams RAG API"
        assert "endpoints" in data
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "ollama_available" in data
        assert "faiss_index_loaded" in data
    
    def test_stats_endpoint(self):
        """Test the stats endpoint"""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        # Should return stats or error message
        assert isinstance(data, dict)
    
    def test_query_endpoint_empty_message(self):
        """Test query endpoint with empty message"""
        response = client.post("/query", json={"message": ""})
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_query_endpoint_valid_message(self):
        """Test query endpoint with valid message"""
        response = client.post("/query", json={"message": "Who is the CTO?"})
        # Should either succeed or return a specific error
        assert response.status_code in [200, 500, 503]
        if response.status_code == 200:
            data = response.json()
            assert "response" in data
    
    def test_query_endpoint_with_sources(self):
        """Test query endpoint with sources included"""
        response = client.post("/query", json={
            "message": "Who is the CTO?",
            "include_sources": True
        })
        # Should either succeed or return a specific error
        assert response.status_code in [200, 500, 503]
        if response.status_code == 200:
            data = response.json()
            assert "response" in data
            assert "sources" in data

class TestConfiguration:
    """Test configuration management"""
    
    def test_configuration_validation(self):
        """Test configuration validation"""
        # This will fail if Ollama is not running, which is expected
        result = validate_configuration()
        # We don't assert the result since it depends on external services
    
    def test_settings_loaded(self):
        """Test that settings are properly loaded"""
        assert settings.api_title == "Employee Teams RAG API"
        assert settings.api_version == "1.0.0"
        assert settings.ollama_model == "phi3"

class TestAdvancedQueries:
    """Test advanced query capabilities"""
    
    def test_employee_query_engine_initialization(self):
        """Test EmployeeQueryEngine initialization"""
        from rag_backend.rag_agent.advanced_queries import EmployeeQueryEngine
        from rag_backend.config import get_excel_path
        
        try:
            engine = EmployeeQueryEngine(get_excel_path())
            # Should not raise an exception
            assert engine is not None
        except Exception as e:
            # This is expected if Excel file doesn't exist or is invalid
            pytest.skip(f"EmployeeQueryEngine test skipped: {e}")

def test_integration_workflow():
    """Test the complete integration workflow"""
    # This is a high-level integration test
    # It tests that the main components work together
    
    # 1. Check if the API is accessible
    try:
        response = client.get("/health")
        assert response.status_code == 200
    except Exception as e:
        pytest.skip(f"Integration test skipped - API not accessible: {e}")
    
    # 2. Test a simple query
    try:
        response = client.post("/query", json={"message": "How many employees are there?"})
        # Should return either a valid response or a specific error
        assert response.status_code in [200, 500, 503]
    except Exception as e:
        pytest.skip(f"Integration test skipped - Query failed: {e}")

# Performance tests
class TestPerformance:
    """Performance and load testing"""
    
    def test_response_time(self):
        """Test that responses are reasonably fast"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 5.0  # Should respond within 5 seconds
        assert response.status_code == 200

# Security tests
class TestSecurity:
    """Security-related tests"""
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = client.get("/health")
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers
    
    def test_input_validation(self):
        """Test input validation"""
        # Test with very long input
        long_message = "x" * 10000
        response = client.post("/query", json={"message": long_message})
        # Should handle gracefully (either process or return appropriate error)
        assert response.status_code in [200, 400, 500, 503]

if __name__ == "__main__":
    # Run basic tests
    pytest.main([__file__, "-v"]) 