from fastapi import FastAPI, HTTPException

from app.models.schemas import TicketRequest, TicketResponse
from app.agent.graph import agent_graph
from app.agent.state import SupportState

app = FastAPI(
    title = "LangGraph Support Agent",
    description= "Customer support triage and resoltuin sysemt built with LangGraph",
    version = "0.1.0"
)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "LangGraph Support Agent is running"
    }

@app.post("/ticket", response_model = TicketResponse)
async def create_ticket(request: TicketRequest):
    """
    Submit a customer support ticket. The agent will:
    1. Classify the intent
    2. Gather relevant information
    3. Attempt resolution
    4. Escalate to human if needed
    """
    try:
        # Build initial state from request

        initial_state: SupportState = {
            "customer_message": request.customer_message,
            "customer_id": request.customer_id,
            "intent": "",
            "confidence": 0.0,
            "gathered_info":{},
            "resolution": "",
            "status": "pending",
            "escalated": False
        }

        final_state = agent_graph.invoke(initial_state)

        import uuid
        ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"

        return TicketResponse(
            ticket_id=ticket_id,
            intent=final_state["intent"],
            confidence=final_state["confidence"],
            resolution=final_state["resolution"],
            status=final_state["status"],
            escalated=final_state["escalated"],
            gathered_info=final_state["gathered_info"],
        )
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))