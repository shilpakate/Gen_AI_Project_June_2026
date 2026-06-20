"""
Financial Risk Analysis Agent
Analyzes financial metrics, debt-to-income ratio, credit risk, and anomalies.
"""

from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("FinancialRiskAnalysisAgent")


@mcp.tool()
def calculate_debt_to_income_ratio(income: float, existing_liabilities: float, loan_amount: float, tenure_months: int) -> dict:
    """
    Calculates the debt-to-income (DTI) ratio including the new loan.

    Args:
        income: Annual income
        existing_liabilities: Existing monthly debt obligations
        loan_amount: Requested loan amount
        tenure_months: Loan tenure in months

    Returns:
        Dictionary with DTI ratio and details
    """
    monthly_income = income / 12
    estimated_monthly_payment = (loan_amount / tenure_months) * 1.05  # Add 5% for interest

    total_monthly_debt = existing_liabilities + estimated_monthly_payment
    dti_ratio = total_monthly_debt / monthly_income if monthly_income > 0 else 1.0

    return {
        "dti_ratio": round(dti_ratio, 3),
        "monthly_income": round(monthly_income, 2),
        "monthly_debt": round(total_monthly_debt, 2),
        "estimated_payment": round(estimated_monthly_payment, 2)
    }


@mcp.tool()
def get_credit_risk_level(credit_score: int) -> str:
    """
    Determines credit risk level based on credit score.

    Args:
        credit_score: Credit score (0-900)

    Returns:
        Risk level: 'Low', 'Medium', 'High'
    """
    if credit_score >= 750:
        return "Low"
    elif credit_score >= 650:
        return "Medium"
    else:
        return "High"


@mcp.tool()
def analyze_loan_amount_risk(loan_amount: float, income: float) -> dict:
    """
    Analyzes risk based on loan-to-income ratio.

    Args:
        loan_amount: Requested loan amount
        income: Annual income

    Returns:
        Dictionary with loan risk analysis
    """
    loan_to_income = loan_amount / income if income > 0 else float('inf')

    if loan_to_income < 1.5:
        risk_level = "Low"
    elif loan_to_income <= 3:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "loan_to_income_ratio": round(loan_to_income, 2),
        "risk_level": risk_level,
        "reason": f"Loan amount is {loan_to_income:.1f}x annual income"
    }


@mcp.tool()
def detect_anomalies(
    income: float,
    loan_amount: float,
    existing_liabilities: float,
    age: int,
    credit_score: int
) -> dict:
    """
    Detects anomalies or red flags in the application.

    Args:
        income: Annual income
        loan_amount: Requested loan amount
        existing_liabilities: Existing monthly debt
        age: Applicant age
        credit_score: Credit score

    Returns:
        Dictionary with anomaly flags
    """
    anomalies = []

    # Check for extremely high debt
    if existing_liabilities > (income / 12) * 0.5:
        anomalies.append("High existing debt relative to income")

    # Check for low credit score
    if credit_score < 600:
        anomalies.append("Low credit score")

    # Check for age-related concerns
    if age < 21:
        anomalies.append("Applicant age below 21")
    elif age > 75:
        anomalies.append("Applicant age above 75")

    # Check for very large loan relative to income
    if loan_amount > income * 4:
        anomalies.append("Loan amount extremely high relative to income")

    # Check for very low income relative to loan
    if income < 30000 and loan_amount > income * 2:
        anomalies.append("Very low income relative to loan amount")

    return {
        "anomalies_detected": len(anomalies) > 0,
        "anomalies": anomalies,
        "risk_level": "High" if len(anomalies) >= 2 else "Medium" if len(anomalies) == 1 else "Low"
    }


@mcp.tool()
def generate_risk_summary(dti_ratio: float, credit_risk: str, loan_risk: str, anomalies: list) -> dict:
    """
    Generates a comprehensive risk summary.

    Args:
        dti_ratio: Debt-to-income ratio
        credit_risk: Credit risk level
        loan_risk: Loan amount risk level
        anomalies: List of detected anomalies

    Returns:
        Risk summary dictionary
    """
    risk_factors = []

    if dti_ratio > 0.5:
        risk_factors.append("High DTI ratio")

    if credit_risk in ["Medium", "High"]:
        risk_factors.append(f"{credit_risk} credit risk")

    if loan_risk in ["Medium", "High"]:
        risk_factors.append(f"{loan_risk} loan amount risk")

    if anomalies:
        risk_factors.extend([f"Anomaly: {a}" for a in anomalies])

    overall_risk = "High" if len(risk_factors) >= 3 else "Medium" if len(risk_factors) >= 1 else "Low"

    return {
        "overall_risk": overall_risk,
        "risk_factors": risk_factors,
        "summary": f"Application presents {overall_risk.lower()} financial risk with {len(risk_factors)} identified factors"
    }


if __name__ == "__main__":
    # Test the MCP server
    dti = calculate_debt_to_income_ratio(75000, 2000, 50000, 60)
    print("DTI Analysis:", dti)

    credit_risk = get_credit_risk_level(750)
    print("Credit Risk:", credit_risk)

    loan_risk = analyze_loan_amount_risk(50000, 75000)
    print("Loan Risk:", loan_risk)

    anomalies = detect_anomalies(75000, 50000, 2000, 35, 750)
    print("Anomalies:", anomalies)

    summary = generate_risk_summary(dti["dti_ratio"], credit_risk, loan_risk["risk_level"], anomalies["anomalies"])
    print("Risk Summary:", summary)
