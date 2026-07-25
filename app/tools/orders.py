"""
Mock order status tool.
In production, this would query your order management system.
"""

MOCK_ORDERS = {
    "ORD-001": {"status": "delivered", "date": "2024-01-10", "item": "Wireless Headphones"},
    "ORD-002": {"status": "shipped", "date": "2024-01-18", "item": "USB-C Hub"},
    "ORD-003": {"status": "processing", "date": "2024-01-20", "item": "Mechanical Keyboard"},
    "ORD-004": {"status": "cancelled", "date": "2024-01-12", "item": "Monitor Stand"},
    "ORD-005": {"status": "returned", "date": "2024-01-05", "item": "Webcam"},
}


def check_order_status(order_id: str) -> dict:
    """
    Check the status of an order by ID.
    Returns order details.
    """
    order = MOCK_ORDERS.get(order_id.upper())

    if not order:
        return {
            "order_id": order_id,
            "found": False,
            "message": "No order found with this ID. Please verify the order number.",
        }

    return {
        "order_id": order_id,
        "found": True,
        **order,
    }