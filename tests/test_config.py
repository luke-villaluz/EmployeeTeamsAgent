"""
Test configuration management
"""
from rag_backend.config import settings, validate_configuration

class TestConfiguration:
    def test_configuration_validation(self):
        result = validate_configuration()
        # No assert, just runs validation

    def test_settings_loaded(self):
        assert settings.api_title == "Employee Teams RAG API"
        assert settings.api_version == "1.0.0"
        assert settings.ollama_model == "phi3" 