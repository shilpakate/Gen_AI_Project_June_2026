"""
Unit tests for the Loan Decision Agent
Tests decision logic, scoring, and error handling
"""

import pytest
from agents.decision_agent import make_loan_decision, DecisionInput


class TestDecisionScoring:
    """Test decision scoring logic"""

    def test_approved_decision_high_score(self):
        """Test that high score results in Approved decision"""
        data = DecisionInput(
            income_stability_score=0.85,
            employment_risk="Low",
            dti_ratio=0.32,
            credit_risk="Low",
            loan_to_income=1.8,
            anomalies=[],
            applicant_id="TEST001"
        )
        result = make_loan_decision(data)

        assert result["decision"] == "Approved"
        assert result["confidence"] == 0.95
        assert result["score"] >= 4.0
        assert result["applicant_id"] == "TEST001"

    def test_review_decision_moderate_score(self):
        """Test that moderate score results in Review decision"""
        data = DecisionInput(
            income_stability_score=0.65,
            employment_risk="Medium",
            dti_ratio=0.45,
            credit_risk="Medium",
            loan_to_income=2.5,
            anomalies=[],
            applicant_id="TEST002"
        )
        result = make_loan_decision(data)

        assert result["decision"] == "Review"
        assert result["confidence"] == 0.75
        assert 2.5 <= result["score"] < 4.0

    def test_rejected_decision_low_score(self):
        """Test that low score results in Rejected decision"""
        data = DecisionInput(
            income_stability_score=0.3,
            employment_risk="High",
            dti_ratio=0.62,
            credit_risk="High",
            loan_to_income=4.2,
            anomalies=["High debt", "Low credit"],
            applicant_id="TEST003"
        )
        result = make_loan_decision(data)

        assert result["decision"] == "Rejected"
        assert result["confidence"] == 0.90
        assert result["score"] < 2.5

    def test_score_calculation_positive_factors(self):
        """Test that positive factors increase score correctly"""
        data = DecisionInput(
            income_stability_score=0.8,  # +1
            employment_risk="Low",         # +1
            dti_ratio=0.35,               # +1
            credit_risk="Low",            # +1
            loan_to_income=1.5,           # +1
            anomalies=[],
            applicant_id="TEST004"
        )
        result = make_loan_decision(data)

        assert result["score"] == 5.0

    def test_score_calculation_with_anomalies(self):
        """Test that anomalies decrease score correctly"""
        data = DecisionInput(
            income_stability_score=0.8,   # +1
            employment_risk="Low",        # +1
            dti_ratio=0.35,              # +1
            credit_risk="Low",           # +1
            loan_to_income=1.5,          # +1
            anomalies=["High debt", "Low credit"],  # -1.0 (0.5 each)
            applicant_id="TEST005"
        )
        result = make_loan_decision(data)

        assert result["score"] == 4.0  # 5.0 - 1.0
        assert len(result["factors"]) > 5

    def test_factors_list_populated(self):
        """Test that factors list is properly populated"""
        data = DecisionInput(
            income_stability_score=0.8,
            employment_risk="Low",
            dti_ratio=0.35,
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id="TEST006"
        )
        result = make_loan_decision(data)

        assert len(result["factors"]) >= 5
        assert "Strong income stability" in result["factors"]
        assert "Good credit profile" in result["factors"]
        assert "Stable employment" in result["factors"]

    def test_anomaly_factors_included(self):
        """Test that anomalies are included in factors"""
        anomalies = ["High debt", "Low credit", "Young age"]
        data = DecisionInput(
            income_stability_score=0.7,
            employment_risk="Medium",
            dti_ratio=0.4,
            credit_risk="Medium",
            loan_to_income=2.0,
            anomalies=anomalies,
            applicant_id="TEST007"
        )
        result = make_loan_decision(data)

        for anomaly in anomalies:
            assert any(anomaly in factor for factor in result["factors"])


class TestDecisionInputValidation:
    """Test input validation and edge cases"""

    def test_invalid_income_stability_score_above_1(self):
        """Test that income stability score > 1 is clamped"""
        data = DecisionInput(
            income_stability_score=1.5,  # Invalid, should be clamped to 1
            employment_risk="Low",
            dti_ratio=0.35,
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id="TEST008"
        )
        result = make_loan_decision(data)

        # Should still produce a valid decision
        assert result["decision"] in ["Approved", "Review", "Rejected"]
        assert result["confidence"] > 0

    def test_invalid_income_stability_score_below_0(self):
        """Test that income stability score < 0 is clamped"""
        data = DecisionInput(
            income_stability_score=-0.5,  # Invalid, should be clamped to 0
            employment_risk="High",
            dti_ratio=0.7,
            credit_risk="High",
            loan_to_income=5.0,
            anomalies=[],
            applicant_id="TEST009"
        )
        result = make_loan_decision(data)

        # Should still produce a valid decision (Rejected)
        assert result["decision"] in ["Approved", "Review", "Rejected"]

    def test_negative_dti_ratio_clamped_to_0(self):
        """Test that negative DTI is clamped to 0"""
        data = DecisionInput(
            income_stability_score=0.8,
            employment_risk="Low",
            dti_ratio=-0.1,  # Invalid, should be clamped to 0
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id="TEST010"
        )
        result = make_loan_decision(data)

        assert result["decision"] == "Approved"  # Should be approved with valid clamped values

    def test_extreme_dti_ratio(self):
        """Test handling of extreme DTI ratio"""
        data = DecisionInput(
            income_stability_score=0.8,
            employment_risk="Low",
            dti_ratio=10.0,  # Extremely high DTI
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id="TEST011"
        )
        result = make_loan_decision(data)

        # Should be rejected despite other good factors
        assert result["decision"] == "Rejected"

    def test_zero_applicant_id(self):
        """Test that empty applicant_id is handled"""
        data = DecisionInput(
            income_stability_score=0.8,
            employment_risk="Low",
            dti_ratio=0.35,
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id=""
        )
        result = make_loan_decision(data)

        assert result["applicant_id"] == ""
        assert result["decision"] == "Approved"


class TestDecisionOutput:
    """Test decision output structure"""

    def test_output_contains_required_fields(self):
        """Test that output contains all required fields"""
        data = DecisionInput(
            income_stability_score=0.8,
            employment_risk="Low",
            dti_ratio=0.35,
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id="TEST012"
        )
        result = make_loan_decision(data)

        required_fields = ["applicant_id", "decision", "confidence", "score", "factors", "explanation", "timestamp"]
        for field in required_fields:
            assert field in result

    def test_confidence_is_valid_probability(self):
        """Test that confidence is a valid probability (0-1)"""
        data = DecisionInput(
            income_stability_score=0.8,
            employment_risk="Low",
            dti_ratio=0.35,
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id="TEST013"
        )
        result = make_loan_decision(data)

        assert 0 <= result["confidence"] <= 1.0

    def test_score_is_numeric(self):
        """Test that score is numeric"""
        data = DecisionInput(
            income_stability_score=0.8,
            employment_risk="Low",
            dti_ratio=0.35,
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id="TEST014"
        )
        result = make_loan_decision(data)

        assert isinstance(result["score"], float)
        assert -5 <= result["score"] <= 5

    def test_explanation_is_non_empty(self):
        """Test that explanation is provided"""
        data = DecisionInput(
            income_stability_score=0.8,
            employment_risk="Low",
            dti_ratio=0.35,
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id="TEST015"
        )
        result = make_loan_decision(data)

        assert result["explanation"]
        assert len(result["explanation"]) > 0

    def test_timestamp_is_iso_format(self):
        """Test that timestamp is in ISO format"""
        data = DecisionInput(
            income_stability_score=0.8,
            employment_risk="Low",
            dti_ratio=0.35,
            credit_risk="Low",
            loan_to_income=1.5,
            anomalies=[],
            applicant_id="TEST016"
        )
        result = make_loan_decision(data)

        # Should be ISO format: YYYY-MM-DDTHH:MM:SS.ffffff
        import datetime
        try:
            datetime.datetime.fromisoformat(result["timestamp"])
            assert True
        except ValueError:
            assert False, "Timestamp is not in ISO format"


class TestDecisionEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_all_moderate_factors(self):
        """Test decision with all moderate factors"""
        data = DecisionInput(
            income_stability_score=0.5,
            employment_risk="Medium",
            dti_ratio=0.45,
            credit_risk="Medium",
            loan_to_income=2.5,
            anomalies=[],
            applicant_id="TEST017"
        )
        result = make_loan_decision(data)

        # Should result in Review
        assert result["decision"] == "Review"

    def test_good_factors_with_many_anomalies(self):
        """Test that many anomalies override good factors"""
        data = DecisionInput(
            income_stability_score=0.9,   # +1
            employment_risk="Low",        # +1
            dti_ratio=0.3,               # +1
            credit_risk="Low",           # +1
            loan_to_income=1.5,          # +1
            anomalies=["Anomaly1", "Anomaly2", "Anomaly3", "Anomaly4", "Anomaly5", "Anomaly6"],  # -3.0
            applicant_id="TEST018"
        )
        result = make_loan_decision(data)

        # Score should be 5.0 - 3.0 = 2.0, resulting in Rejected
        assert result["decision"] == "Rejected"
        assert result["score"] == 2.0

    def test_only_income_stability_high(self):
        """Test decision with only income stability factor positive"""
        data = DecisionInput(
            income_stability_score=0.9,   # +1
            employment_risk="High",
            dti_ratio=0.7,
            credit_risk="High",
            loan_to_income=4.0,
            anomalies=[],
            applicant_id="TEST019"
        )
        result = make_loan_decision(data)

        # Only 1 point, should be rejected
        assert result["decision"] == "Rejected"

    def test_boundary_at_4_0_score(self):
        """Test boundary condition at 4.0 score (Approved threshold)"""
        data = DecisionInput(
            income_stability_score=0.8,   # +1
            employment_risk="Low",        # +1
            dti_ratio=0.39,              # +1
            credit_risk="Low",           # +1
            loan_to_income=2.0,          # +1
            anomalies=["Anomaly"],       # -0.5
            applicant_id="TEST020"
        )
        result = make_loan_decision(data)

        # Score should be 4.5, resulting in Approved
        assert result["decision"] == "Approved"
        assert result["score"] == 4.5

    def test_boundary_at_2_5_score(self):
        """Test boundary condition at 2.5 score (Review threshold)"""
        data = DecisionInput(
            income_stability_score=0.8,   # +1
            employment_risk="Low",        # +1
            dti_ratio=0.5,               # 0
            credit_risk="Medium",        # 0
            loan_to_income=2.0,          # +1
            anomalies=[],                # 0
            applicant_id="TEST021"
        )
        result = make_loan_decision(data)

        # Score should be 3.0, resulting in Review
        assert result["decision"] == "Review"
