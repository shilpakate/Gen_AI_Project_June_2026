import os
import logging
from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

client = Anthropic()

# Circuit breaker for API failures
class CircuitBreaker:
    def __init__(self, failure_threshold=3, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.is_open = False

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = __import__("time").time()
        if self.failure_count >= self.failure_threshold:
            self.is_open = True
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")

    def record_success(self):
        self.failure_count = 0
        self.is_open = False

    def can_attempt(self):
        if not self.is_open:
            return True
        elapsed = __import__("time").time() - self.last_failure_time
        if elapsed > self.timeout:
            self.is_open = False
            self.failure_count = 0
            logger.info("Circuit breaker reset")
            return True
        return False

claude_circuit_breaker = CircuitBreaker()

# Fallback explanations for different decisions
FALLBACK_EXPLANATIONS = {
    "Approved": "Your loan application has been approved. You meet the key lending criteria with strong financial metrics. You will receive further details via email or contact our support team for questions.",
    "Review": "Your loan application requires manual review by our lending team. Some factors warrant additional consideration. We will contact you within 2-3 business days with next steps.",
    "Rejected": "Unfortunately, your loan application has not been approved at this time. This decision is based on financial metrics that do not align with our lending criteria. We encourage you to reapply after improving your financial profile."
}

def generate_explanation(profile: dict, risk: dict, decision: str) -> str:
    """
    Uses Claude to generate an explanation for a loan decision.
    Falls back to template if Claude API fails.

    Args:
        profile: Applicant profile data (income_score, employment)
        risk: Risk analysis data (dti, credit)
        decision: The decision made (Approved, Rejected, Review)

    Returns:
        Explanation string from Claude or fallback template
    """
    # Check circuit breaker
    if not claude_circuit_breaker.can_attempt():
        logger.warning("Claude API circuit breaker open, using fallback explanation")
        return FALLBACK_EXPLANATIONS.get(decision, "Your loan decision has been made. Contact support for details.")

    prompt = f"""
    Based on the following loan application analysis, provide a brief, clear explanation
    for why the loan decision was {decision}.

    Applicant Profile:
    - Income Stability Score: {profile.get('income_score', 'N/A')}
    - Employment Type Risk: {profile.get('employment', 'N/A')}

    Financial Risk Metrics:
    - Debt-to-Income Ratio: {risk.get('dti', 'N/A')}
    - Credit Risk Level: {risk.get('credit', 'N/A')}

    Decision: {decision}

    Provide a 2-3 sentence explanation suitable for the applicant.
    """

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            messages=[
                {"role": "user", "content": prompt}
            ],
            timeout=10.0  # 10 second timeout
        )
        claude_circuit_breaker.record_success()
        logger.info(f"Claude API call successful for {decision} decision")
        return message.content[0].text

    except RateLimitError as e:
        logger.warning(f"Claude API rate limit hit: {e}")
        claude_circuit_breaker.record_failure()
        return FALLBACK_EXPLANATIONS.get(decision, "Your loan decision has been made. Contact support for details.")

    except APIConnectionError as e:
        logger.error(f"Claude API connection error: {e}")
        claude_circuit_breaker.record_failure()
        return FALLBACK_EXPLANATIONS.get(decision, "Your loan decision has been made. Contact support for details.")

    except APIError as e:
        logger.error(f"Claude API error: {e}")
        claude_circuit_breaker.record_failure()
        return FALLBACK_EXPLANATIONS.get(decision, "Your loan decision has been made. Contact support for details.")

    except Exception as e:
        logger.error(f"Unexpected error generating explanation: {e}")
        return FALLBACK_EXPLANATIONS.get(decision, "Your loan decision has been made. Contact support for details.")

if __name__ == "__main__":
    # Test the function
    test_profile = {"income_score": 0.8, "employment": "Low"}
    test_risk = {"dti": 0.35, "credit": "Low"}
    explanation = generate_explanation(test_profile, test_risk, "Approved")
    print("Generated Explanation:")
    print(explanation)
