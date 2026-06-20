"""
Pytest configuration and fixtures for Loan Approval System tests
"""

import pytest
import logging
from pathlib import Path


@pytest.fixture(scope="session")
def setup_logging():
    """Setup logging for test session"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


@pytest.fixture
def sample_strong_applicant():
    """Fixture for strong applicant data"""
    return {
        "applicant_id": "TEST_STRONG",
        "age": 35,
        "annual_income": 75000,
        "credit_score": 750,
        "existing_liabilities": 2000,
        "employment_type": "Full-time",
        "employment_years": 8,
        "loan_amount": 50000,
        "tenure_months": 60,
        "contact_email": "strong@example.com"
    }


@pytest.fixture
def sample_moderate_applicant():
    """Fixture for moderate applicant data"""
    return {
        "applicant_id": "TEST_MODERATE",
        "age": 28,
        "annual_income": 55000,
        "credit_score": 680,
        "existing_liabilities": 3000,
        "employment_type": "Contract",
        "employment_years": 3,
        "loan_amount": 45000,
        "tenure_months": 60,
        "contact_email": "moderate@example.com"
    }


@pytest.fixture
def sample_weak_applicant():
    """Fixture for weak applicant data"""
    return {
        "applicant_id": "TEST_WEAK",
        "age": 22,
        "annual_income": 28000,
        "credit_score": 580,
        "existing_liabilities": 8000,
        "employment_type": "Self-employed",
        "employment_years": 1,
        "loan_amount": 60000,
        "tenure_months": 60,
        "contact_email": "weak@example.com"
    }


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset mocks before each test"""
    yield
    # Cleanup after test if needed


def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Auto-mark integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        # Auto-mark unit tests
        elif "test_" in item.nodeid and "agent" in item.nodeid:
            item.add_marker(pytest.mark.unit)
