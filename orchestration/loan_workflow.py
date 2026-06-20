"""
LangGraph-based Loan Application Workflow Orchestration
Implements state machine pattern for loan decision process
"""

from typing import TypedDict, Optional, Annotated
from datetime import datetime
from langgraph.graph import StateGraph, START, END

# Import agent functions
from mcp_servers.applicant_agent import (
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


class LoanApplicationState(TypedDict):
    """
    Complete state for loan application workflow.
    Carries all data through the state machine.
    """
    # Input Parameters
    applicant_id: str
    age: int
    annual_income: float
    credit_score: int
    existing_liabilities: float
    employment_type: str
    employment_years: int
    loan_amount: float
    tenure_months: int
    location: Optional[str]
    contact_email: Optional[str]

    # Stage 1: Applicant Analysis Results
    income_stability: float
    employment_risk: str
    credit_summary: str

    # Stage 2: Financial Risk Analysis Results
    dti_ratio: float
    monthly_income: float
    monthly_debt: float
    credit_risk: str
    loan_to_income_ratio: float
    loan_risk_level: str
    anomalies: list
    risk_factors: list
    overall_risk: str

    # Stage 3: Decision Results
    decision: str
    confidence: float
    score: float
    factors: list
    explanation: str
    timestamp: str

    # Stage 4: Compliance Results
    case_id: str
    notification_status: str


def applicant_analysis_node(state: LoanApplicationState) -> dict:
    """
    Node 1: Applicant Profile Analysis

    Extracts and analyzes applicant information:
    - Income stability score
    - Employment risk level
    - Credit history summary
    """
    print(f"📊 [NODE 1] Analyzing applicant profile for {state['applicant_id']}...")

    # Calculate income stability
    income_stability = calculate_income_stability_score(
        income=state["annual_income"],
        employment_type=state["employment_type"],
        employment_years=state["employment_years"]
    )

    # Assess employment risk
    employment_risk = get_employment_risk(
        employment_type=state["employment_type"],
        employment_years=state["employment_years"]
    )

    # Get credit history summary
    credit_summary = get_credit_history_summary(credit_score=state["credit_score"])

    print(f"   ✓ Income Stability: {income_stability:.2f}")
    print(f"   ✓ Employment Risk: {employment_risk}")
    print(f"   ✓ Credit Summary: {credit_summary}")

    return {
        "income_stability": income_stability,
        "employment_risk": employment_risk,
        "credit_summary": credit_summary
    }


def risk_analysis_node(state: LoanApplicationState) -> dict:
    """
    Node 2: Financial Risk Analysis

    Calculates financial metrics and risk levels:
    - Debt-to-income ratio
    - Credit risk level
    - Loan-to-income ratio
    - Anomalies detection
    """
    print(f"💰 [NODE 2] Analyzing financial risk...")

    # Calculate DTI ratio
    dti_result = calculate_debt_to_income_ratio(
        income=state["annual_income"],
        existing_liabilities=state["existing_liabilities"],
        loan_amount=state["loan_amount"],
        tenure_months=state["tenure_months"]
    )

    # Get credit risk level
    credit_risk = get_credit_risk_level(credit_score=state["credit_score"])

    # Analyze loan amount risk
    loan_risk = analyze_loan_amount_risk(
        loan_amount=state["loan_amount"],
        income=state["annual_income"]
    )

    # Detect anomalies
    anomalies_result = detect_anomalies(
        income=state["annual_income"],
        loan_amount=state["loan_amount"],
        existing_liabilities=state["existing_liabilities"],
        age=state["age"],
        credit_score=state["credit_score"]
    )

    # Generate risk summary
    risk_summary = generate_risk_summary(
        dti_ratio=dti_result["dti_ratio"],
        credit_risk=credit_risk,
        loan_risk=loan_risk["risk_level"],
        anomalies=anomalies_result["anomalies"]
    )

    print(f"   ✓ DTI Ratio: {dti_result['dti_ratio']:.3f}")
    print(f"   ✓ Credit Risk: {credit_risk}")
    print(f"   ✓ Loan-to-Income: {loan_risk['loan_to_income_ratio']:.2f}x")
    print(f"   ✓ Anomalies: {len(anomalies_result['anomalies'])} detected")
    print(f"   ✓ Overall Risk: {risk_summary['overall_risk']}")

    return {
        "dti_ratio": dti_result["dti_ratio"],
        "monthly_income": dti_result["monthly_income"],
        "monthly_debt": dti_result["monthly_debt"],
        "credit_risk": credit_risk,
        "loan_to_income_ratio": loan_risk["loan_to_income_ratio"],
        "loan_risk_level": loan_risk["risk_level"],
        "anomalies": anomalies_result["anomalies"],
        "risk_factors": risk_summary["risk_factors"],
        "overall_risk": risk_summary["overall_risk"]
    }


def decision_node(state: LoanApplicationState) -> dict:
    """
    Node 3: Loan Decision Making

    Makes final approval decision with:
    - Scoring algorithm (0-5 points)
    - Decision classification
    - Claude-powered explanation
    - Confidence level
    """
    print(f"⚖️  [NODE 3] Making loan decision...")

    # Prepare decision input
    decision_input = DecisionInput(
        income_stability_score=state["income_stability"],
        employment_risk=state["employment_risk"],
        dti_ratio=state["dti_ratio"],
        credit_risk=state["credit_risk"],
        loan_to_income=state["loan_to_income_ratio"],
        anomalies=state["anomalies"],
        applicant_id=state["applicant_id"]
    )

    # Make decision
    decision_result = make_loan_decision(decision_input)

    print(f"   ✓ Decision: {decision_result['decision']}")
    print(f"   ✓ Score: {decision_result['score']:.1f}/5")
    print(f"   ✓ Confidence: {decision_result['confidence']:.1%}")
    print(f"   ✓ Factors: {len(decision_result['factors'])} identified")

    return {
        "decision": decision_result["decision"],
        "confidence": decision_result["confidence"],
        "score": decision_result["score"],
        "factors": decision_result["factors"],
        "explanation": decision_result["explanation"],
        "timestamp": decision_result["timestamp"]
    }


def compliance_node(state: LoanApplicationState) -> dict:
    """
    Node 4: Compliance & Notifications

    Handles post-decision operations:
    - Creates case record
    - Logs decision for audit trail
    - Sends notifications
    - Updates compliance tracking
    """
    print(f"📋 [NODE 4] Processing compliance & notifications...")

    # Create case record
    case_record = create_case_record(
        applicant_id=state["applicant_id"],
        decision=state["decision"],
        confidence=state["confidence"],
        risk_level=state["overall_risk"]
    )

    # Log decision for audit trail
    log_decision(
        applicant_id=state["applicant_id"],
        decision=state["decision"],
        risk_level=state["overall_risk"],
        explanation=state["explanation"]
    )

    # Send notification
    notification_result = send_notification(
        applicant_id=state["applicant_id"],
        decision=state["decision"],
        explanation=state["explanation"],
        contact_email=state["contact_email"]
    )

    print(f"   ✓ Case ID: {case_record['case_id']}")
    print(f"   ✓ Decision logged for audit trail")
    print(f"   ✓ Notification: {notification_result.get('status', 'sent')}")

    return {
        "case_id": case_record["case_id"],
        "notification_status": notification_result.get("status", "sent")
    }


def create_loan_workflow() -> StateGraph:
    """
    Creates the LangGraph state machine for loan application workflow.

    Workflow Structure:
    START
      ↓
    [1] Applicant Analysis → Income stability, employment risk, credit
      ↓
    [2] Risk Analysis → DTI, credit risk, loan-to-income, anomalies
      ↓
    [3] Decision → Approval/Rejection/Review + explanation
      ↓
    [4] Compliance → Logging, notifications, case management
      ↓
    END

    Returns:
        Compiled StateGraph ready for invocation
    """
    # Create the state graph
    graph = StateGraph(LoanApplicationState)

    # Add nodes for each stage
    graph.add_node("applicant_analysis", applicant_analysis_node)
    graph.add_node("risk_analysis", risk_analysis_node)
    graph.add_node("decision", decision_node)
    graph.add_node("compliance", compliance_node)

    # Define workflow edges (sequence of execution)
    graph.add_edge(START, "applicant_analysis")
    graph.add_edge("applicant_analysis", "risk_analysis")
    graph.add_edge("risk_analysis", "decision")
    graph.add_edge("decision", "compliance")
    graph.add_edge("compliance", END)

    # Compile and return
    compiled_graph = graph.compile()

    print("✅ LangGraph Workflow Created:")
    print("   Nodes: [1] Applicant Analysis → [2] Risk Analysis → [3] Decision → [4] Compliance")
    print("   State Machine: Fully orchestrated with state persistence")

    return compiled_graph


# Global workflow instance
loan_workflow = create_loan_workflow()


def run_loan_application(
    applicant_id: str,
    age: int,
    annual_income: float,
    credit_score: int,
    existing_liabilities: float,
    employment_type: str,
    employment_years: int,
    loan_amount: float,
    tenure_months: int,
    location: Optional[str] = None,
    contact_email: Optional[str] = None
) -> dict:
    """
    Execute the complete loan application workflow.

    This is the main entry point for processing a loan application.
    The workflow proceeds through 4 stages automatically with state management.

    Args:
        applicant_id: Unique applicant identifier
        age: Applicant age
        annual_income: Annual income in dollars
        credit_score: Credit score (0-900)
        existing_liabilities: Existing monthly debt obligations
        employment_type: Type of employment (Full-time, Contract, etc.)
        employment_years: Years in current employment
        loan_amount: Requested loan amount
        tenure_months: Loan repayment period in months
        location: Applicant location (optional)
        contact_email: Contact email for notifications (optional)

    Returns:
        dict: Complete workflow result with decision and case details
    """
    # Prepare initial state
    initial_state: LoanApplicationState = {
        "applicant_id": applicant_id,
        "age": age,
        "annual_income": annual_income,
        "credit_score": credit_score,
        "existing_liabilities": existing_liabilities,
        "employment_type": employment_type,
        "employment_years": employment_years,
        "loan_amount": loan_amount,
        "tenure_months": tenure_months,
        "location": location,
        "contact_email": contact_email,
        # Initialize other fields as None/empty
        "income_stability": 0.0,
        "employment_risk": "",
        "credit_summary": "",
        "dti_ratio": 0.0,
        "monthly_income": 0.0,
        "monthly_debt": 0.0,
        "credit_risk": "",
        "loan_to_income_ratio": 0.0,
        "loan_risk_level": "",
        "anomalies": [],
        "risk_factors": [],
        "overall_risk": "",
        "decision": "",
        "confidence": 0.0,
        "score": 0.0,
        "factors": [],
        "explanation": "",
        "timestamp": "",
        "case_id": "",
        "notification_status": ""
    }

    print(f"\n🚀 Starting Loan Application Workflow for {applicant_id}")
    print(f"━" * 60)

    # Invoke workflow
    final_state = loan_workflow.invoke(initial_state)

    print(f"━" * 60)
    print(f"✅ Workflow Complete!")
    print(f"   Final Decision: {final_state['decision']}")
    print(f"   Case ID: {final_state['case_id']}\n")

    return final_state


if __name__ == "__main__":
    # Test the workflow
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
        contact_email="app001@example.com"
    )

    print("\nWorkflow Result:")
    print(f"  Decision: {result['decision']}")
    print(f"  Confidence: {result['confidence']:.1%}")
    print(f"  Case ID: {result['case_id']}")
    print(f"  Explanation: {result['explanation'][:100]}...")
