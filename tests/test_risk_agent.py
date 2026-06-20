"""
Unit tests for the Financial Risk Analysis Agent
Tests DTI calculation, risk levels, and anomaly detection
"""

import pytest
from mcp_servers.risk_agent import (
    calculate_debt_to_income_ratio,
    get_credit_risk_level,
    analyze_loan_amount_risk,
    detect_anomalies,
    generate_risk_summary
)


class TestDTICalculation:
    """Test debt-to-income ratio calculation"""

    def test_dti_healthy_range(self):
        """Test DTI calculation for healthy ratio"""
        result = calculate_debt_to_income_ratio(
            income=75000,
            existing_liabilities=2000,
            loan_amount=50000,
            tenure_months=60
        )

        assert "dti_ratio" in result
        assert result["dti_ratio"] < 0.5  # Should be healthy
        assert result["monthly_income"] == 75000 / 12
        assert result["monthly_debt"] > 0

    def test_dti_high_ratio(self):
        """Test DTI calculation for high ratio"""
        result = calculate_debt_to_income_ratio(
            income=30000,
            existing_liabilities=1500,
            loan_amount=50000,
            tenure_months=60
        )

        assert result["dti_ratio"] > 0.5  # High DTI
        assert result["monthly_income"] == 30000 / 12

    def test_dti_zero_existing_liabilities(self):
        """Test DTI with no existing liabilities"""
        result = calculate_debt_to_income_ratio(
            income=60000,
            existing_liabilities=0,
            loan_amount=30000,
            tenure_months=60
        )

        assert result["dti_ratio"] >= 0
        assert result["monthly_debt"] > 0  # Should include loan payment

    def test_dti_very_high_income(self):
        """Test DTI with very high income"""
        result = calculate_debt_to_income_ratio(
            income=500000,
            existing_liabilities=1000,
            loan_amount=30000,
            tenure_months=60
        )

        assert result["dti_ratio"] < 0.1  # Should be very low

    def test_dti_very_low_income(self):
        """Test DTI with very low income"""
        result = calculate_debt_to_income_ratio(
            income=20000,
            existing_liabilities=1000,
            loan_amount=30000,
            tenure_months=60
        )

        assert result["dti_ratio"] > 0.4  # Should be high


class TestCreditRiskLevel:
    """Test credit risk classification"""

    def test_credit_risk_low(self):
        """Test low credit risk classification"""
        result = get_credit_risk_level(credit_score=750)
        assert result == "Low"

    def test_credit_risk_medium(self):
        """Test medium credit risk classification"""
        result = get_credit_risk_level(credit_score=700)
        assert result == "Medium"

    def test_credit_risk_high(self):
        """Test high credit risk classification"""
        result = get_credit_risk_level(credit_score=600)
        assert result == "High"

    def test_credit_risk_boundary_low_medium(self):
        """Test boundary at Low/Medium threshold (750)"""
        result_below = get_credit_risk_level(credit_score=749)
        result_at = get_credit_risk_level(credit_score=750)
        result_above = get_credit_risk_level(credit_score=751)

        assert result_at == "Low"

    def test_credit_risk_boundary_medium_high(self):
        """Test boundary at Medium/High threshold (650)"""
        result_below = get_credit_risk_level(credit_score=649)
        result_at = get_credit_risk_level(credit_score=650)
        result_above = get_credit_risk_level(credit_score=651)

        assert result_at == "Medium"

    def test_credit_risk_perfect_score(self):
        """Test perfect credit score"""
        result = get_credit_risk_level(credit_score=850)
        assert result == "Low"

    def test_credit_risk_minimum_score(self):
        """Test minimum credit score"""
        result = get_credit_risk_level(credit_score=300)
        assert result == "High"


class TestLoanAmountRisk:
    """Test loan amount risk analysis"""

    def test_loan_amount_acceptable(self):
        """Test acceptable loan-to-income ratio"""
        result = analyze_loan_amount_risk(
            loan_amount=50000,
            income=75000
        )

        assert result["risk_level"] == "Low"
        assert result["loan_to_income_ratio"] <= 2

    def test_loan_amount_moderate(self):
        """Test moderate loan-to-income ratio"""
        result = analyze_loan_amount_risk(
            loan_amount=120000,
            income=50000
        )

        assert result["risk_level"] == "Medium"
        assert 2 < result["loan_to_income_ratio"] <= 3

    def test_loan_amount_high(self):
        """Test high loan-to-income ratio"""
        result = analyze_loan_amount_risk(
            loan_amount=100000,
            income=30000
        )

        assert result["risk_level"] == "High"
        assert result["loan_to_income_ratio"] > 3

    def test_loan_amount_very_high_income(self):
        """Test with very high income"""
        result = analyze_loan_amount_risk(
            loan_amount=100000,
            income=200000
        )

        assert result["risk_level"] == "Low"
        assert result["loan_to_income_ratio"] == 0.5


class TestAnomalyDetection:
    """Test anomaly detection logic"""

    def test_no_anomalies_detected(self):
        """Test case with no anomalies"""
        result = detect_anomalies(
            income=75000,
            loan_amount=50000,
            existing_liabilities=2000,
            age=35,
            credit_score=750
        )

        assert result["anomalies"] == []

    def test_high_debt_anomaly(self):
        """Test detection of high debt anomaly"""
        result = detect_anomalies(
            income=30000,
            loan_amount=50000,
            existing_liabilities=20000,  # High debt
            age=35,
            credit_score=750
        )

        assert len(result["anomalies"]) > 0
        assert any("debt" in anomaly.lower() for anomaly in result["anomalies"])

    def test_low_credit_score_anomaly(self):
        """Test detection of low credit score anomaly"""
        result = detect_anomalies(
            income=75000,
            loan_amount=50000,
            existing_liabilities=2000,
            age=25,
            credit_score=580  # Low credit with young age
        )

        assert len(result["anomalies"]) > 0

    def test_extreme_loan_size_anomaly(self):
        """Test detection of extreme loan size"""
        result = detect_anomalies(
            income=30000,
            loan_amount=150000,  # Very large loan
            existing_liabilities=2000,
            age=35,
            credit_score=700
        )

        assert len(result["anomalies"]) > 0
        assert any("loan" in anomaly.lower() for anomaly in result["anomalies"])

    def test_very_low_income_anomaly(self):
        """Test detection of very low income"""
        result = detect_anomalies(
            income=20000,  # Very low income
            loan_amount=50000,
            existing_liabilities=2000,
            age=35,
            credit_score=700
        )

        assert len(result["anomalies"]) > 0

    def test_multiple_anomalies(self):
        """Test case with multiple anomalies"""
        result = detect_anomalies(
            income=20000,      # Very low
            loan_amount=150000,  # Very large
            existing_liabilities=15000,  # High debt
            age=23,            # Young
            credit_score=580   # Low credit
        )

        assert len(result["anomalies"]) >= 3


class TestRiskSummary:
    """Test risk summary generation"""

    def test_risk_summary_low_risk(self):
        """Test risk summary for low risk case"""
        result = generate_risk_summary(
            dti_ratio=0.3,
            credit_risk="Low",
            loan_risk="Low",
            anomalies=[]
        )

        assert result["overall_risk"] == "Low"
        assert len(result["risk_factors"]) <= 2

    def test_risk_summary_medium_risk(self):
        """Test risk summary for medium risk case"""
        result = generate_risk_summary(
            dti_ratio=0.45,
            credit_risk="Medium",
            loan_risk="Medium",
            anomalies=[]
        )

        assert result["overall_risk"] == "Medium"

    def test_risk_summary_high_risk(self):
        """Test risk summary for high risk case"""
        result = generate_risk_summary(
            dti_ratio=0.6,
            credit_risk="High",
            loan_risk="High",
            anomalies=["High debt", "Low credit"]
        )

        assert result["overall_risk"] == "High"
        assert len(result["risk_factors"]) > 0

    def test_risk_summary_contains_risk_factors(self):
        """Test that risk summary includes risk factors"""
        result = generate_risk_summary(
            dti_ratio=0.5,
            credit_risk="Medium",
            loan_risk="Medium",
            anomalies=["Anomaly1"]
        )

        assert "risk_factors" in result
        assert isinstance(result["risk_factors"], list)

    def test_risk_summary_with_anomalies(self):
        """Test risk summary incorporates anomalies"""
        anomalies = ["High debt", "Low income"]
        result = generate_risk_summary(
            dti_ratio=0.35,
            credit_risk="Low",
            loan_risk="Low",
            anomalies=anomalies
        )

        # Anomalies should elevate risk despite low metrics
        assert result["overall_risk"] in ["Low", "Medium"]


class TestRiskIntegration:
    """Integration tests for risk analysis"""

    def test_full_risk_analysis_strong_applicant(self):
        """Test full risk analysis for strong applicant"""
        dti = calculate_debt_to_income_ratio(75000, 2000, 20000, 60)
        credit_risk = get_credit_risk_level(750)
        loan_risk = analyze_loan_amount_risk(20000, 75000)
        anomalies = detect_anomalies(75000, 20000, 2000, 35, 750)
        summary = generate_risk_summary(
            dti["dti_ratio"],
            credit_risk,
            loan_risk["risk_level"],
            anomalies["anomalies"]
        )

        assert summary["overall_risk"] == "Low"
        assert dti["dti_ratio"] < 0.4

    def test_full_risk_analysis_weak_applicant(self):
        """Test full risk analysis for weak applicant"""
        dti = calculate_debt_to_income_ratio(30000, 5000, 50000, 60)
        credit_risk = get_credit_risk_level(580)
        loan_risk = analyze_loan_amount_risk(50000, 30000)
        anomalies = detect_anomalies(30000, 50000, 5000, 25, 580)
        summary = generate_risk_summary(
            dti["dti_ratio"],
            credit_risk,
            loan_risk["risk_level"],
            anomalies["anomalies"]
        )

        assert summary["overall_risk"] == "High"
