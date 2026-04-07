import anthropic
import json
import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic()

# Haiku pricing (per million tokens)
HAIKU_INPUT_COST  = 0.80  / 1_000_000
HAIKU_OUTPUT_COST = 4.00  / 1_000_000

def router_node(state: dict) -> dict:
    """
    Node A: Cheap router. Decides if this is a chat or research query.
    Uses Claude Haiku to keep costs minimal.
    """
    print(f"[Router] Classifying query: '{state['query']}'")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=10,
        system="""You are a query classifier.
        Respond with ONLY one word: 'research' or 'chat'.

        'research' = needs web search, current events, facts, data
        'chat' = general conversation, opinions, simple questions""",
        messages=[{"role": "user", "content": state["query"]}]
    )

    input_tokens  = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    node_cost = (input_tokens * HAIKU_INPUT_COST) + (output_tokens * HAIKU_OUTPUT_COST)

    route = response.content[0].text.strip().lower()
    print(f"[Router] Route: {route} | Cost: ${node_cost:.6f}")

    return {
        "route": route,
        "total_cost": state["total_cost"] + node_cost
    }


def route_decision(state: dict) -> str:
    """Edge function: tells LangGraph where to go after the router."""
    if state["route"] == "research":
        return "researcher"
    else:
        return "chat_responder"


def chat_responder_node(state: dict) -> dict:
    """Simple chat — no search, no loops, cheap."""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": state["query"]}]
    )

    input_tokens  = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    node_cost = (input_tokens * HAIKU_INPUT_COST) + (output_tokens * HAIKU_OUTPUT_COST)

    return {
        "final_answer": response.content[0].text,
        "total_cost": state["total_cost"] + node_cost
    }