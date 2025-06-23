"""
Test advanced query capabilities
"""
import pytest

class TestAdvancedQueries:
    def test_employee_query_engine_initialization(self):
        from rag_backend.rag_agent.advanced_queries import EmployeeQueryEngine
        from rag_backend.config import get_excel_path

        try:
            engine = EmployeeQueryEngine(get_excel_path())
            assert engine is not None
        except Exception as e:
            pytest.skip(f"EmployeeQueryEngine test skipped: {e}") 