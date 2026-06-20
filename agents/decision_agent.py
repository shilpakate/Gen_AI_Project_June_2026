"""
Loan Decision Agent
Makes final approval/rejection/review decision based on all analysis.
"""

import logging
from fastmcp import FastMCP
from pydantic import BaseModel
from utils.claude_client import generate_explanation

logger = logging.getLogger(__name__)

mcp = FastMCP("LoanDecisionAgent")


class DecisionInput(BaseModel):
    """Input data for decision making"""
    income_stability_score: float
    employment_risk: str
    dti_ratio: float
    credit_risk: str
    loan_to_income: float
    anomalies: list
    applicant_id: str


@mcp.tool()
def make_loan_decision(data: DecisionInput) -> dict:
    """
    Makes a loan approval decision based on comprehensive analysis.
    Includes error handling for all edge cases.

    Args:
        data: DecisionInput containing all analysis metrics

    Returns:
        Dictionary with decision, confidence, factors, and explanation
    """
    try:
        # Validate input data
        if data.income_stability_score < 0 or data.income_stability_score > 1:
            logger.warning(f"Invalid income_stability_score: {data.income_stability_score}")
            data.income_stability_score = max(0, min(1, data.income_stability_score))

        if data.dti_ratio < 0:
            logger.warning(f"Invalid dti_ratio: {data.dti_ratio}")
            data.dti_ratio = 0

        if data.loan_to_income < 0:
            logger.warning(f"Invalid loan_to_income: {data.loan_to_income}")
            data.loan_to_income = 0

        score = 0
        factors = []

        # Income stability evaluation (max +1)
        if data.income_stability_score > 0.7:
            score += 1
            factors.append("Strong income stability")
        elif data.income_stability_score > 0.4:
            score += 0.5
            factors.append("Moderate income stability")
        else:
            factors.append("Weak income stability")

        # Credit risk evaluation (max +1)
        if data.credit_risk == "Low":
            score += 1
            factors.append("Good credit profile")
        elif data.credit_risk == "Medium":
            score += 0.5
            factors.append("Fair credit profile")
        else:
            factors.append("Poor credit profile")

        # DTI ratio evaluation (max +1, penalties for extreme values)
        if data.dti_ratio < 0.4:
            score += 1
            factors.append("Healthy debt-to-income ratio")
        elif data.dti_ratio < 0.5:
            score += 0.5
            factors.append("Acceptable debt-to-income ratio")
        elif data.dti_ratio < 0.8:
            factors.append("High debt-to-income ratio")
        else:
            score -= 2
            factors.append("Critically high debt-to-income ratio")

        # Employment risk evaluation (max +1)
        if data.employment_risk == "Low":
            score += 1
            factors.append("Stable employment")
        elif data.employment_risk == "Medium":
            score += 0.5
            factors.append("Moderate employment stability")
        else:
            factors.append("Unstable employment")

        # Loan-to-income evaluation (max +1)
        if data.loan_to_income <= 2:
            score += 1
            factors.append("Loan amount appropriate for income")
        elif data.loan_to_income <= 5:
            score += 0.5
            factors.append("Loan amount manageable")
        else:
            factors.append("Loan amount high relative to income")

        # Anomaly check (penalty)
        if data.anomalies:
            factors.extend([f"⚠️ {anomaly}" for anomaly in data.anomalies])
            score -= len(data.anomalies) * 0.5

        # Ensure score stays in valid range
        score = max(-5, min(5, score))

        # Determine decision based on score
        if score >= 4:
            decision = "Approved"
            confidence = 0.95
        elif score >= 2.5:
            decision = "Review"
            confidence = 0.75
        else:
            decision = "Rejected"
            confidence = 0.90

        # Generate explanation using Claude (with error handling)
        try:
            explanation = generate_explanation(
                profile={
                    "income_score": data.income_stability_score,
                    "employment": data.employment_risk
                },
                risk={
                    "dti": data.dti_ratio,
                    "credit": data.credit_risk
                },
                decision=decision
            )
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            explanation = f"Your loan decision has been made as {decision}. Contact support for details."

        logger.info(f"Decision made for {data.applicant_id}: {decision} (score={score:.2f})")

        return {
            "applicant_id": data.applicant_id,
            "decision": decision,
            "confidence": min(confidence, 1.0),
            "score": float(round(score, 2)),
            "factors": factors,
            "explanation": explanation,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Critical error in make_loan_decision: {e}", exc_info=True)
        # Fallback decision
        return {
            "applicant_id": data.applicant_id,
            "decision": "Review",
            "confidence": 0.5,
            "score": 0.0,
            "factors": ["System error: Manual review required"],
            "explanation": "An error occurred during processing. Your application has been routed for manual review.",
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Test the decision agent
    test_input = DecisionInput(
        income_stability_score=0.8,
        employment_risk="Low",
        dti_ratio=0.35,
        credit_risk="Low",
        loan_to_income=2.5,
        anomalies=[],
        applicant_id="APP001"
    )

    decision = make_loan_decision(test_input)
    print("Decision Result:")
    for key, value in decision.items():
        print(f"  {key}: {value}")
