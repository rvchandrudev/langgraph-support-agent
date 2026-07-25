"""
Mock payment history tool.
In production, this would call a real payment processor API (Stripe, etc.).
"""

MOCK_PAYMENTS = {
    "cust_123": [
        {"date": "2024-01-15", "amount": 29.99, "description": "Monthly Subscription", "status": "completed"},
        {"date": "2024-01-15", "amount": 29.99, "description": "Monthly Subscription", "status": "completed"},
        {"date": "2023-12-15", "amount": 29.99, "description": "Monthly Subscription", "status": "completed"},
    ],
    "cust_456": [
        {"date": "2024-01-10", "amount": 99.00, "description": "Annual Subscription", "status": "completed"},
        {"date": "2024-01-11", "amount": 15.00, "description": "Add-on Storage", "status": "completed"},
    ],
    "cust_789": [
        {"date": "2024-01-01", "amount": 49.99, "description": "Pro Plan Upgrade", "status": "completed"},
        {"date": "2024-01-05", "amount": 49.99, "description": "Pro Plan Upgrade", "status": "completed"},
        {"date": "2024-01-05", "amount": 49.99, "description": "Pro Plan Upgrade", "status": "completed"},
    ],
}


def check_payment_history(customer_id: str) -> dict:
    """
    Retrieve the last 5 payments transactions for a customer.
    Returns a dict with the transaction history
    """

    transactions = MOCK_PAYMENTS.get(customer_id, [])

    if not transactions:
        return {
            "customer_id": customer_id,
            "transactional_count": 0,
            "transactions": [],
            "message": "No payment history found for this customer"
        }

    return {
        "customer_id": customer_id,
        "transaction_count": len(transactions),
        "transactions" : transactions[-5:]
    }