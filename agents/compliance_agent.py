"""
Compliance & Action Orchestrator Agent
Handles notifications, case management, and compliance logging.
"""

from fastmcp import FastMCP
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

mcp = FastMCP("ComplianceOrchestratorAgent")


class ComplianceAction(BaseModel):
    """Input for compliance and notification actions"""
    applicant_id: str
    decision: str
    confidence: float
    risk_level: str


# Mock notification system (in production, this would send emails, SMS, etc.)
NOTIFICATION_LOG = []


@mcp.tool()
def log_decision(applicant_id: str, decision: str, risk_level: str, explanation: str) -> dict:
    """
    Logs the decision for compliance and audit purposes.

    Args:
        applicant_id: Unique applicant identifier
        decision: Decision made (Approved, Rejected, Review)
        risk_level: Overall risk assessment
        explanation: Explanation of the decision

    Returns:
        Logging confirmation
    """
    case_id = f"CASE-{applicant_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    log_entry = {
        "case_id": case_id,
        "applicant_id": applicant_id,
        "decision": decision,
        "risk_level": risk_level,
        "explanation": explanation,
        "timestamp": datetime.now().isoformat(),
        "status": "logged"
    }

    # In production, this would write to a database or audit log
    NOTIFICATION_LOG.append(log_entry)

    return {
        "status": "success",
        "case_id": case_id,
        "message": f"Decision logged for applicant {applicant_id}"
    }


@mcp.tool()
def send_notification(applicant_id: str, decision: str, explanation: str, contact_email: Optional[str] = None) -> dict:
    """
    Sends notification to the applicant about the decision.

    Args:
        applicant_id: Unique applicant identifier
        decision: Decision made
        explanation: Decision explanation
        contact_email: Email to send notification to

    Returns:
        Notification status
    """
    notification = {
        "applicant_id": applicant_id,
        "decision": decision,
        "explanation": explanation,
        "email": contact_email or f"{applicant_id}@example.com",
        "timestamp": datetime.now().isoformat(),
        "status": "sent"
    }

    NOTIFICATION_LOG.append(notification)

    return {
        "status": "success",
        "notification_id": f"NOTIF-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "message": f"Notification sent to {notification['email']}",
        "decision": decision
    }


@mcp.tool()
def create_case_record(applicant_id: str, decision: str, confidence: float, risk_level: str) -> dict:
    """
    Creates a case record for case management system.

    Args:
        applicant_id: Unique applicant identifier
        decision: Decision made
        confidence: Confidence level in the decision
        risk_level: Risk assessment level

    Returns:
        Case record details
    """
    case_id = f"CASE-{applicant_id}-{datetime.now().strftime('%Y%m%d')}"

    # Determine if case needs manual review
    needs_review = decision == "Review" or confidence < 0.7 or risk_level == "High"

    case_record = {
        "case_id": case_id,
        "applicant_id": applicant_id,
        "decision": decision,
        "confidence": confidence,
        "risk_level": risk_level,
        "needs_review": needs_review,
        "assigned_to": "review_queue" if needs_review else "auto_processing",
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }

    NOTIFICATION_LOG.append(case_record)

    return case_record


@mcp.tool()
def get_compliance_summary() -> dict:
    """
    Returns a summary of all logged decisions and notifications.

    Returns:
        Compliance summary
    """
    approvals = sum(1 for log in NOTIFICATION_LOG if log.get("decision") == "Approved")
    rejections = sum(1 for log in NOTIFICATION_LOG if log.get("decision") == "Rejected")
    reviews = sum(1 for log in NOTIFICATION_LOG if log.get("decision") == "Review")

    return {
        "total_cases": len(NOTIFICATION_LOG),
        "approvals": approvals,
        "rejections": rejections,
        "reviews": reviews,
        "approval_rate": round(approvals / len(NOTIFICATION_LOG) * 100, 2) if NOTIFICATION_LOG else 0,
        "logs": NOTIFICATION_LOG[-10:]  # Last 10 entries
    }


if __name__ == "__main__":
    # Test the compliance agent
    log_result = log_decision(
        "APP001",
        "Approved",
        "Low",
        "Strong income stability and good credit profile"
    )
    print("Log Result:", log_result)

    notify_result = send_notification(
        "APP001",
        "Approved",
        "Your loan application has been approved!"
    )
    print("Notification Result:", notify_result)

    case_result = create_case_record(
        "APP001",
        "Approved",
        0.95,
        "Low"
    )
    print("Case Record:", case_result)

    summary = get_compliance_summary()
    print("Compliance Summary:", summary)
