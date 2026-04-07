from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from agent.nodes import (
    router_node, route_decision,
    chat_responder_node,
    researcher_node, needs_more_research
)
from agent.budget import check_budget, budget_gate

class AgentState(TypedDict):
    query: str
    messages: List[dict]
    search_results: List[str]
    total_cost: float
    iteration: int
    route: str
    final_answer: str
    budget_exceeded: bool
    awaiting_approval: bool

def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("router",         router_node)
    graph.add_node("chat_responder", chat_responder_node)
    graph.add_node("researcher",     researcher_node)
    graph.add_node("budget_check",   check_budget)

    # Entry point
    graph.set_entry_point("router")

    # Router → chat or budget check first
    graph.add_conditional_edges("router", route_decision, {
        "researcher":     "budget_check",
        "chat_responder": "chat_responder"
    })

    # Budget check → researcher or end
    graph.add_conditional_edges("budget_check", budget_gate, {
        "researcher": "researcher",
        "end":        END
    })

    # Researcher → loop back through budget, or end
    graph.add_conditional_edges("researcher", needs_more_research, {
        "budget_check": "budget_check",
        "end":          END
    })

    graph.add_edge("chat_responder", END)

    return graph.compile()