from typing import TypedDict, Optional

class SupportState(TypedDict):
    """State that flows through the agent graph"""
    customer_message: str
    customer_id: Optional[str]
    intent: str
    confidence: float
    gathered_info: dict
    resolution: str
    status: str
    escalated: bool