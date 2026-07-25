from langgraph.graph import StateGraph, END

from app.agent.state import SupportState
from app.agent.nodes import classify_intent, gather_information,attempt_resolution,escalate_to_human


def route_after_resolution(state: SupportState) -> str:
    """
    After resolution attempt, decide: resolved or escalated.
    """

    if state["escalated"]:
        return "escalate_to_human"
    return "end"

def build_graph() -> StateGraph:
    """
    Build and compile the customer support agent graph.
    """

    workflow = StateGraph(SupportState)

    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("gather_information", gather_information)
    workflow.add_node("attempt_resolution", attempt_resolution)
    workflow.add_node("escalate_to_human", escalate_to_human)

    workflow.set_entry_point("classify_intent")

    workflow.add_edge("classify_intent", "gather_information")
    workflow.add_edge("gather_information", "attempt_resolution")

    workflow.add_conditional_edges(
        "attempt_resolution",
        route_after_resolution,
        {
            "end": END,
            "escalate_to_human" : "escalate_to_human"
        }
    )

    workflow.add_edge("escalate_to_human", END)

    return workflow.compile()

agent_graph = build_graph()