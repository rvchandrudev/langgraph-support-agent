"""
Mock account verification tool.
In production, this would query your user database.
"""

MOCK_ACCOUNTS = {
    "cust_123": {
        "status": "active",
        "verified": True,
        "plan": "Monthly Premium",
        "member_since": "2023-06-15",
        "last_login": "2024-01-20",
    },
    "cust_456": {
        "status": "active",
        "verified": True,
        "plan": "Annual Pro",
        "member_since": "2022-03-01",
        "last_login": "2024-01-21",
    },
    "cust_789": {
        "status": "locked",
        "verified": True,
        "plan": "Monthly Pro",
        "member_since": "2023-11-10",
        "last_login": "2024-01-15",
        "lock_reason": "Too many failed login attempts",
    },
    "cust_999": {
        "status": "inactive",
        "verified": False,
        "plan": "Free",
        "member_since": "2024-01-01",
        "last_login": "2024-01-02",
    },
}


def verify_account(customer_id: str) -> dict:
    """
    Verify account status and details.
    Returns account information.
    """
    account = MOCK_ACCOUNTS.get(customer_id)

    if not account:
        return {
            "customer_id": customer_id,
            "found": False,
            "message": "No account found for this customer ID.",
        }

    return {
        "customer_id": customer_id,
        "found": True,
        **account,
    }
