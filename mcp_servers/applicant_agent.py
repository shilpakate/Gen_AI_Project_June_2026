"""
Applicant Profile Agent
Fetches and analyzes applicant data from a mock database.
Calculates income stability, employment risk, credit history summary.
"""

from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

mcp = FastMCP("ApplicantProfileAgent")

class ApplicantData(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    existing_liabilities: float
    application_timestamp: str


# Mock database for applicants
MOCK_APPLICANTS = {
    "APP001": {
        "age": 35,
        "income": 75000,
        "employment_type": "Full-time",
        "credit_score": 750,
        "existing_liabilities": 25000,
        "employment_years": 8
    },
    "APP002": {
        "age": 28,
        "income": 45000,
        "employment_type": "Contract",
        "credit_score": 620,
        "existing_liabilities": 35000,
        "employment_years": 2
    },
    "APP003": {
        "age": 45,
        "income": 120000,
        "employment_type": "Full-time",
        "credit_score": 800,
        "existing_liabilities": 50000,
        "employment_years": 15
    }
}


@mcp.tool()
def fetch_applicant_profile(applicant_id: str) -> dict:
    """
    Fetches applicant profile from the database.

    Args:
        applicant_id: Unique applicant identifier

    Returns:
        Applicant profile data
    """
    if applicant_id not in MOCK_APPLICANTS:
        return {"error": f"Applicant {applicant_id} not found"}

    profile = MOCK_APPLICANTS[applicant_id]
    return {
        "applicant_id": applicant_id,
        "status": "found",
        "profile": profile
    }


@mcp.tool()
def calculate_income_stability_score(income: float, employment_type: str, employment_years: int) -> float:
    """
    Calculates income stability score based on employment type and years.

    Args:
        income: Annual income
        employment_type: Type of employment (Full-time, Contract, Self-employed, etc.)
        employment_years: Years in current employment

    Returns:
        Stability score from 0.0 to 1.0
    """
    score = 0.0

    # Employment type factor
    employment_factors = {
        "Full-time": 0.5,
        "Contract": 0.3,
        "Self-employed": 0.2,
        "Part-time": 0.1
    }
    score += employment_factors.get(employment_type, 0.1)

    # Employment longevity factor
    if employment_years >= 5:
        score += 0.3
    elif employment_years >= 2:
        score += 0.15
    else:
        score += 0.0

    # Income level factor
    if income >= 100000:
        score += 0.2
    elif income >= 50000:
        score += 0.1
    else:
        score += 0.0

    return min(score, 1.0)


@mcp.tool()
def get_employment_risk(employment_type: str, employment_years: int) -> str:
    """
    Categorizes employment risk based on employment type and stability.

    Args:
        employment_type: Type of employment
        employment_years: Years in current employment

    Returns:
        Risk level: 'Low', 'Medium', 'High'
    """
    if employment_type == "Full-time" and employment_years >= 2:
        return "Low"
    elif employment_type in ["Contract", "Self-employed"] and employment_years >= 3:
        return "Medium"
    elif employment_type == "Part-time":
        return "High"
    else:
        return "Medium"


@mcp.tool()
def get_credit_history_summary(credit_score: int) -> str:
    """
    Provides a brief credit history summary based on credit score.

    Args:
        credit_score: Credit score (0-900)

    Returns:
        Summary string
    """
    if credit_score >= 750:
        return "Excellent credit history with consistent payment records"
    elif credit_score >= 650:
        return "Good credit history with few delinquencies"
    elif credit_score >= 550:
        return "Fair credit history with some payment issues"
    else:
        return "Poor credit history with significant payment issues"


if __name__ == "__main__":
    # Test the MCP server
    profile = fetch_applicant_profile("APP001")
    print("Fetched Profile:", profile)

    if "error" not in profile:
        p = profile["profile"]
        income_score = calculate_income_stability_score(
            p["income"], p["employment_type"], p["employment_years"]
        )
        print(f"Income Stability Score: {income_score}")

        emp_risk = get_employment_risk(p["employment_type"], p["employment_years"])
        print(f"Employment Risk: {emp_risk}")

        credit_summary = get_credit_history_summary(p["credit_score"])
        print(f"Credit Summary: {credit_summary}")
