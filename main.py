"""
FastAPI Microservice for Loan Approval System
Coordinates between UI, orchestration engine (LangGraph), and agents.

Uses LangGraph state machine pattern for workflow orchestration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import LangGraph workflow (new)
from orchestration.loan_workflow import run_loan_application

# Keep agent imports for backwards compatibility and direct testing
from mcp_servers.applicant_agent import (
    fetch_applicant_profile,
    calculate_income_stability_score,
    get_employment_risk,
    get_credit_history_summary
)
from mcp_servers.risk_agent import (
    calculate_debt_to_income_ratio,
    get_credit_risk_level,
    analyze_loan_amount_risk,
    detect_anomalies,
    generate_risk_summary
)
from agents.decision_agent import DecisionInput, make_loan_decision
from agents.compliance_agent import (
    log_decision,
    send_notification,
    create_case_record,
    get_compliance_summary
)

app = FastAPI(title="Loan Approval System", version="1.0.0")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoanApplication(BaseModel):
    """Loan application data"""
    applicant_id: str
    age: int
    annual_income: float
    credit_score: int
    existing_liabilities: float
    employment_type: str
    employment_years: int
    location: Optional[str] = None
    loan_amount: float
    tenure_months: int
    contact_email: Optional[str] = None


class ApplicationResponse(BaseModel):
    """Response for loan application"""
    case_id: str
    decision: str
    confidence: float
    risk_level: str
    explanation: str
    factors: list
    timestamp: str


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Loan Approval System"}


@app.post("/apply")
async def process_loan_application(app_request: LoanApplication) -> ApplicationResponse:
    """
    Main endpoint for processing loan applications.
    Uses LangGraph state machine for orchestration.

    Workflow:
    1. Applicant Profile Analysis → income stability, employment risk
    2. Financial Risk Analysis → DTI, credit risk, anomalies
    3. Loan Decision → approval/rejection/review + explanation
    4. Compliance → case creation, logging, notifications

    Args:
        app_request: Loan application data

    Returns:
        Decision and analysis results
    """
    try:
        applicant_id = app_request.applicant_id

        # Validate applicant ID - only allow sample IDs
        valid_ids = ["APP001", "APP002", "APP003"]
        if applicant_id not in valid_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid Applicant ID. Only {', '.join(valid_ids)} are available for testing."
            )

        # ========== LangGraph Workflow Orchestration ==========
        # Execute the complete workflow through the state machine
        final_state = run_loan_application(
            applicant_id=applicant_id,
            age=app_request.age,
            annual_income=app_request.annual_income,
            credit_score=app_request.credit_score,
            existing_liabilities=app_request.existing_liabilities,
            employment_type=app_request.employment_type,
            employment_years=app_request.employment_years,
            loan_amount=app_request.loan_amount,
            tenure_months=app_request.tenure_months,
            location=app_request.location,
            contact_email=app_request.contact_email
        )

        # ========== Return Response ==========
        return ApplicationResponse(
            case_id=final_state["case_id"],
            decision=final_state["decision"],
            confidence=final_state["confidence"],
            risk_level=final_state["overall_risk"],
            explanation=final_state["explanation"],
            factors=final_state["factors"],
            timestamp=final_state["timestamp"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing application: {str(e)}")


@app.get("/compliance-summary")
def get_summary():
    """Get compliance summary"""
    return get_compliance_summary()


@app.get("/status/{applicant_id}")
def get_application_status(applicant_id: str):
    """Get status of a loan application"""
    summary = get_compliance_summary()
    matching_cases = [
        case for case in summary.get("logs", [])
        if case.get("applicant_id") == applicant_id
    ]
    if not matching_cases:
        raise HTTPException(status_code=404, detail="Application not found")
    return matching_cases[-1]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
