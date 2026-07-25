"""
Refund policy tool.
In production, this would query a policy database or config service.
"""

REFUND_POLICIES = {
    "duplicate_charge": {
        "eligible": True,
        "timeframe": "5-10 business days",
        "policy": "Duplicate charges are fully refunded. No action needed from the customer. Refunds are processed automatically.",
    },
    "subscription_cancel": {
        "eligible": False,
        "policy": "Subscriptions can be cancelled anytime, but no refunds are provided for partial months. Access continues until end of billing period.",
    },
    "annual_plan_downgrade": {
        "eligible": False,
        "policy": "Annual plan downgrades take effect at the next renewal date. No partial refunds for the remaining period.",
    },
    "technical_issue": {
        "eligible": True,
        "timeframe": "5-10 business days",
        "policy": "If the service was unavailable due to a confirmed technical issue on our end, you may be eligible for a service credit or partial refund.",
    },
    "fraudulent_charge": {
        "eligible": True,
        "timeframe": "immediate investigation, refund within 24 hours if confirmed",
        "policy": "Report fraudulent charges immediately. Our fraud team investigates within 2 hours. Confirmed fraud results in full refund and account security measures.",
    },
}


def check_refund_policy(issue_type: str) -> dict:
    """
    Check the refund policy for a specific issue type.
    Returns eligibility and policy details.
    """
    policy = REFUND_POLICIES.get(issue_type)

    if not policy:
        return {
            "issue_type": issue_type,
            "eligible": False,
            "policy": "No specific refund policy found for this issue type. Please contact support for manual review.",
        }

    return {
        "issue_type": issue_type,
        **policy,
    }
