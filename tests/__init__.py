"""
Loan Approval System Test Suite

This package contains comprehensive tests for the Loan Approval System.

Test Structure:
  - test_decision_agent.py: Unit tests for decision agent scoring and validation
  - test_risk_agent.py: Unit tests for risk analysis and DTI calculations
  - test_integration.py: End-to-end workflow integration tests
  - conftest.py: Pytest configuration and fixtures

Running Tests:
  # Run all tests
  pytest

  # Run only unit tests
  pytest -m unit

  # Run only integration tests
  pytest -m integration

  # Run specific test file
  pytest tests/test_decision_agent.py

  # Run with verbose output
  pytest -v

  # Run with coverage report
  pytest --cov=. --cov-report=html

Coverage Target:
  - Decision Agent: 95%+ coverage
  - Risk Agent: 90%+ coverage
  - Integration Tests: 85%+ coverage
"""
