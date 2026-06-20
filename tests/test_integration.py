"""
Integration tests for the Loan Approval System
Tests end-to-end workflow and component interactions
"""

import pytest
from orchestration.loan_workflow import run_loan_application


class TestWorkflowIntegration:
    """Integration tests for complete workflow"""

    def test_end_to_end_approved_application(self):
        """Test complete workflow for approved application"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Verify complete workflow result
        assert result["decision"] == "Approved"
        assert result["confidence"] >= 0.9
        assert result["case_id"].startswith("CASE-")
        assert result["applicant_id"] == "APP001"
        assert len(result["factors"]) > 0
        assert result["explanation"]
        assert result["timestamp"]

    def test_end_to_end_review_application(self):
        """Test complete workflow for review application"""
        result = run_loan_application(
            applicant_id="APP002",
            age=28,
            annual_income=65000,
            credit_score=680,
            existing_liabilities=1500,
            employment_type="Contract",
            employment_years=3,
            loan_amount=45000,
            tenure_months=60,
            contact_email="test2@example.com"
        )

        assert result["decision"] == "Review"
        assert 0.5 <= result["confidence"] <= 0.9
        assert result["case_id"].startswith("CASE-")

    def test_end_to_end_rejected_application(self):
        """Test complete workflow for rejected application"""
        result = run_loan_application(
            applicant_id="APP003",
            age=22,
            annual_income=28000,
            credit_score=580,
            existing_liabilities=8000,
            employment_type="Self-employed",
            employment_years=1,
            loan_amount=60000,
            tenure_months=60,
            contact_email="test3@example.com"
        )

        assert result["decision"] == "Rejected"
        assert result["confidence"] >= 0.85
        assert result["case_id"].startswith("CASE-")

    def test_workflow_state_completeness(self):
        """Test that workflow populates all state fields"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Verify all expected fields are present
        required_fields = [
            "applicant_id", "decision", "confidence", "score",
            "factors", "explanation", "timestamp", "case_id",
            "income_stability", "employment_risk", "credit_risk",
            "dti_ratio", "loan_to_income_ratio", "overall_risk"
        ]

        for field in required_fields:
            assert field in result, f"Missing field: {field}"

    def test_workflow_handles_missing_email(self):
        """Test workflow with missing contact email"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email=None
        )

        assert result["decision"] in ["Approved", "Review", "Rejected"]
        assert result["case_id"].startswith("CASE-")

    def test_workflow_handles_missing_location(self):
        """Test workflow with missing location"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            location=None
        )

        assert result["decision"] in ["Approved", "Review", "Rejected"]


class TestWorkflowSequencing:
    """Test proper sequencing of workflow nodes"""

    def test_applicant_node_output_available_to_risk_node(self):
        """Verify applicant node results available to risk node"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Verify applicant node outputs are in result
        assert "income_stability" in result
        assert "employment_risk" in result
        assert result["income_stability"] > 0

    def test_risk_node_output_available_to_decision_node(self):
        """Verify risk node results available to decision node"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Verify risk node outputs are in result
        assert "dti_ratio" in result
        assert "credit_risk" in result
        assert "overall_risk" in result

    def test_decision_node_output_available_to_compliance_node(self):
        """Verify decision node results available to compliance node"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Verify decision node outputs are available
        assert "decision" in result
        assert "score" in result
        assert "factors" in result

    def test_compliance_node_output_generated(self):
        """Verify compliance node generates case record"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Verify compliance node outputs
        assert result["case_id"]
        assert result["case_id"].startswith("CASE-")
        assert "timestamp" in result


class TestWorkflowErrorScenarios:
    """Test workflow behavior under error conditions"""

    def test_workflow_with_extreme_age(self):
        """Test workflow handles extreme age values"""
        result = run_loan_application(
            applicant_id="APP001",
            age=150,  # Extreme value
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Should still produce decision
        assert result["decision"] in ["Approved", "Review", "Rejected"]

    def test_workflow_with_zero_income(self):
        """Test workflow handles zero income"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=0,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Should result in rejection
        assert result["decision"] in ["Rejected", "Review"]

    def test_workflow_with_negative_loan_amount(self):
        """Test workflow handles negative loan amount"""
        try:
            result = run_loan_application(
                applicant_id="APP001",
                age=35,
                annual_income=75000,
                credit_score=750,
                existing_liabilities=2000,
                employment_type="Full-time",
                employment_years=8,
                loan_amount=-50000,  # Negative
                tenure_months=60,
                contact_email="test@example.com"
            )
            # If it doesn't error, should produce valid decision
            assert result["decision"] in ["Approved", "Review", "Rejected"]
        except Exception:
            # Validation error is acceptable
            pass

    def test_workflow_with_very_long_tenure(self):
        """Test workflow with extreme tenure"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=600,  # Very long (50 years)
            contact_email="test@example.com"
        )

        # Should still produce decision
        assert result["decision"] in ["Approved", "Review", "Rejected"]


class TestCaseIDGeneration:
    """Test case ID generation and uniqueness"""

    def test_case_id_format(self):
        """Test case ID follows expected format"""
        result = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        case_id = result["case_id"]
        assert case_id.startswith("CASE-")
        assert "APP001" in case_id

    def test_case_ids_different_for_different_applicants(self):
        """Test that different applicants get different case IDs"""
        result1 = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        result2 = run_loan_application(
            applicant_id="APP002",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Case IDs should be different
        assert result1["case_id"] != result2["case_id"]
        assert "APP001" in result1["case_id"]
        assert "APP002" in result2["case_id"]


class TestDecisionConsistency:
    """Test that decisions are consistent for same inputs"""

    def test_same_inputs_produce_same_decision(self):
        """Test that identical inputs produce same decision"""
        result1 = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        result2 = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Decisions should be the same
        assert result1["decision"] == result2["decision"]
        assert result1["score"] == result2["score"]

    def test_minor_income_difference_consistent_decision(self):
        """Test that small income changes don't drastically change decisions"""
        result_75k = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=75000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        result_76k = run_loan_application(
            applicant_id="APP001",
            age=35,
            annual_income=76000,
            credit_score=750,
            existing_liabilities=2000,
            employment_type="Full-time",
            employment_years=8,
            loan_amount=50000,
            tenure_months=60,
            contact_email="test@example.com"
        )

        # Decision should remain same for minor income change
        assert result_75k["decision"] == result_76k["decision"]
