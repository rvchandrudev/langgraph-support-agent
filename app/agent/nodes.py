import json
import uuid
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.agent.state import SupportState
from app.config import settings
from app.tools.knowledge_base import search_knowledge_base
from app.tools.payments import check_payment_history
from app.tools.refunds import check_refund_policy
from app.tools.accounts import verify_account
from app.tools.orders import check_order_status

# LLM instance
llm = ChatGroq(
    model=settings.llm_model,
    api_key=settings.groq_api_key,
    temperature=0.0,
)


# ---------- NODE 1: CLASSIFY INTENT ----------

def classify_intent(state: SupportState) -> SupportState:
    """
    Analyze the customer message and classify the intent.
    """
    prompt = f"""Classify this customer support message into one intent.

Return ONLY a JSON object. Do not include any other text.

Example: {{"intent": "billing", "confidence": 0.95}}

Intent options:
- billing: Payment issues, charges, refunds, invoices
- technical: App errors, bugs, how-to questions
- account: Login issues, password resets, account locked
- general: Business hours, contact info, other

Customer message: {state["customer_message"]}

JSON:"""

    response = llm.invoke([HumanMessage(content=prompt)])
    response_text = response.content.strip()

    # Try to extract JSON from the response
    try:
        # Sometimes LLMs wrap JSON in ```json blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        result = json.loads(response_text)
        state["intent"] = result.get("intent", "general")
        state["confidence"] = result.get("confidence", 0.5)
    except (json.JSONDecodeError, IndexError):
        # Fallback: extract intent from text
        response_lower = response_text.lower()
        if "billing" in response_lower:
            state["intent"] = "billing"
        elif "technical" in response_lower:
            state["intent"] = "technical"
        elif "account" in response_lower:
            state["intent"] = "account"
        else:
            state["intent"] = "general"
        state["confidence"] = 0.5

    return state


# ---------- NODE 2: GATHER INFORMATION ----------

def gather_information(state: SupportState) -> SupportState:
    """
    Call relevant tools based on the classified intent.
    """
    intent = state["intent"]
    customer_id = state.get("customer_id", "cust_123")
    customer_message = state["customer_message"]
    gathered = {}

    if intent == "billing":
        gathered["payment_history"] = check_payment_history(customer_id)
        gathered["refund_policy"] = check_refund_policy("duplicate_charge")

    elif intent == "technical":
        gathered["knowledge_base"] = search_knowledge_base(customer_message)

    elif intent == "account":
        gathered["account_info"] = verify_account(customer_id)
        gathered["knowledge_base"] = search_knowledge_base(customer_message)

    elif intent == "general":
        gathered["knowledge_base"] = search_knowledge_base(customer_message)

    state["gathered_info"] = gathered
    return state


# ---------- NODE 3: ATTEMPT RESOLUTION ----------

def attempt_resolution(state: SupportState) -> SupportState:
    """
    Generate a resolution based on gathered information.
    """
    prompt = f"""You are a customer support agent. Generate a resolution based on the information below.

If you can resolve the issue, end your response with: STATUS: RESOLVED
If you cannot resolve, end with: STATUS: ESCALATE

Customer message: {state["customer_message"]}
Intent: {state["intent"]}
Gathered information: {state["gathered_info"]}

Your response:"""

    response = llm.invoke([HumanMessage(content=prompt)])
    response_text = response.content

    if "STATUS: RESOLVED" in response_text:
        state["status"] = "resolved"
        state["escalated"] = False
        state["resolution"] = response_text.replace("STATUS: RESOLVED", "").strip()
    elif "STATUS: ESCALATE" in response_text:
        state["status"] = "escalated"
        state["escalated"] = True
        state["resolution"] = response_text.replace("STATUS: ESCALATE", "").strip()
    else:
        # Fallback: check if response contains a resolution
        if len(response_text) > 20:
            state["status"] = "resolved"
            state["escalated"] = False
            state["resolution"] = response_text
        else:
            state["status"] = "escalated"
            state["escalated"] = True
            state["resolution"] = "Unable to generate resolution. Human review required."

    return state


# ---------- NODE 4: ESCALATE TO HUMAN ----------

def escalate_to_human(state: SupportState) -> SupportState:
    """
    Format a ticket for human agent review.
    """
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"

    summary = f"""=== ESCALATED TICKET ===
Ticket ID: {ticket_id}
Intent: {state["intent"]} (Confidence: {state["confidence"]})
Customer ID: {state.get("customer_id", "N/A")}

Original Message:
{state["customer_message"]}

Gathered Information:
{state["gathered_info"]}

AI Attempted Resolution:
{state["resolution"]}

Reason for Escalation:
The AI could not resolve this issue automatically. Human review is required.

=== END TICKET ===
"""
    state["status"] = "escalated"
    state["escalated"] = True
    state["resolution"] = summary

    return state