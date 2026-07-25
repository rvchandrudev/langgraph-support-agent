from pydantic import BaseModel, Field
from typing import Optional

class TicketRequest(BaseModel):
    customer_message: str = Field(..., min_length=1, max_length=2000)
    customer_id: Optional[str] = None

class TicketResponse(BaseModel):
    ticket_id: str
    intent: str
    confidence: float
    resolution: str
    status: str
    escalated: bool
    gathered_info: dict
