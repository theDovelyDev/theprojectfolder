from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    query: str                  # Original user question
    messages: List[dict]        # Conversation history
    search_results: List[str]   # Accumulated search results
    total_cost: float           # Running cost tracker
    iteration: int              # Loop counter
    route: str                  # "chat" or "research"
    final_answer: str           # Output to user
    budget_exceeded: bool       # Kill switch flag
    awaiting_approval: bool     # Human-in-the-loop flag

from agent.nodes import router_node, route_decision, chat_responder_node

def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("chat_responder", chat_responder_node)

    # Set entry point
    graph.set_entry_point("router")

    # Conditional edge from router — research goes to END for now (Phase 4 placeholder)
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "researcher":     END,   # placeholder until Phase 4
            "chat_responder": "chat_responder"
        }
    )

    graph.add_edge("chat_responder", END)

    return graph.compile()