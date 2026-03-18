# Budget-Conscious Research Agent
## Project Zero: AI/ML Portfolio Project

**Tagline:** A research agent that stops and asks permission before spending your money.  
**Estimated Time:** 10–14 hours  
**Difficulty:** Intermediate (with guidance)  
**Tech Stack:** Python, LangGraph, Anthropic API, Tavily Search, AWS Lambda / Fargate  

---

## Project Overview

**The Problem:** AI agents can run up API costs fast — especially research agents that loop through multiple searches. Most tutorials show you how to build the agent. Nobody shows you how to put a budget guardrail on it.

**The Solution:** A LangGraph research agent with a `check_budget()` kill switch that interrupts execution, reports cost to the user, and asks for permission before spending more.

**The FinOps Angle:** The same pattern that controls this $0.05 research budget is the same pattern that controls $50,000 AI inference budgets at enterprise scale. This project demonstrates that thinking at a small, observable level.

**Key Metrics (Target):**
- Routing cost per query: < $0.001 (Haiku)
- Research cost per query: ~$0.02–0.04 (Sonnet)
- Budget interrupt threshold: $0.05 (configurable)
- Max iterations guardrail: 3

---

## Architecture

```
User Query
    ↓
Node A: Router (Claude Haiku — cheap)
    ├── "Chat" → Direct response, no search, ~$0.001
    └── "Research" → Node B
            ↓
Node B: Researcher (Claude Sonnet + Tavily Search)
            ↓
    check_budget(state)
            ├── cost < $0.05 → Loop back if needed
            └── cost ≥ $0.05 → INTERRUPT
                        ↓
                Human-in-the-loop: "Spend another $0.05?"
                        ├── Yes → Resume
                        └── No  → Return results so far
```

### Component Decisions

| Component | Choice | Why |
|-----------|--------|-----|
| Orchestrator | LangGraph | Visual graph = clear view of where money flows |
| Router Model | Claude Haiku | Cheapest Anthropic model, same SDK you already know |
| Research Model | Claude Sonnet 4 | Best reasoning for actual deep research |
| Search Tool | Tavily API | Built for LLM agents, clean output, free tier available |
| Budget Guardrail | `check_budget()` | Python function, runs before every loop |
| Loop Guardrail | `max_iterations = 3` | Prevents infinite loops on bad search results |
| Deployment | AWS Fargate | Stateful agent needs persistent runtime — no Lambda timeout issues |

---

## Cost Model

### Per-Query Cost Breakdown

| Step | Model | Avg Tokens | Cost |
|------|-------|-----------|------|
| Routing | Claude Haiku | ~200 in / 50 out | ~$0.0001 |
| Research (1 loop) | Claude Sonnet | ~1,500 in / 500 out | ~$0.018 |
| Research (2 loops) | Claude Sonnet | ~3,000 in / 1,000 out | ~$0.036 |
| Search | Tavily | — | $0.00 (free tier: 1,000/mo) |
| **Budget trigger** | — | — | **$0.05 threshold** |

### Development Cost Estimate

| Phase | Estimated API Cost |
|-------|--------------------|
| Phase 1–2 (setup, local dev) | $0.00 |
| Phase 3 (LangGraph + routing) | ~$0.50 |
| Phase 4 (research + budget logic) | ~$1.00 |
| Phase 5 (testing 50 queries) | ~$2.00 |
| Phase 6 (deployment) | ~$0.50 |
| **Total Estimate** | **~$4.00** |

**Budget alert:** Set Anthropic spend limit to $10 during development.

---

## Phase 1: Environment Setup (1–2 hours)

### 1.1 Accounts & API Keys Needed
- [ ] Anthropic API key (you have this from IDP Pipeline)
- [ ] Tavily API key — free at [tavily.com](https://tavily.com) (1,000 searches/month free)
- [ ] AWS account (you have this)

### 1.2 Project Structure
```
budget-research-agent/
├── agent/
│   ├── __init__.py
│   ├── graph.py          ← LangGraph graph definition
│   ├── nodes.py          ← Node A (router) + Node B (researcher)
│   ├── budget.py         ← check_budget() function
│   └── tools.py          ← Tavily search tool wrapper
├── tests/
│   └── test_agent.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### 1.3 Install Dependencies
```bash
pip install langgraph langchain-anthropic tavily-python python-dotenv
```

### 1.4 Environment Variables
```bash
# .env.example (commit this)
ANTHROPIC_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
MAX_BUDGET=0.05
MAX_ITERATIONS=3
```

---

## Phase 2: Understand LangGraph (1 hour)

Before writing code, understand the two core concepts:

**State** — A Python dictionary that gets passed between every node. Think of it as the agent's memory for one conversation.

```python
# This is what flows through your graph
state = {
    "query": "What is FinOps?",
    "messages": [],
    "search_results": [],
    "total_cost": 0.0,
    "iteration": 0,
    "needs_more_research": False
}
```

**Nodes** — Python functions that receive state, do something, and return updated state.

```python
def my_node(state):
    # do something
    return {"total_cost": state["total_cost"] + 0.001}
```

**Edges** — Connections between nodes. Can be fixed (`A always goes to B`) or conditional (`A goes to B or C depending on state`).

That's the whole mental model. Your graph is just: state flows in → node updates it → edge decides where it goes next.

---

## Phase 3: Build the Router Node (2–3 hours)

### 3.1 Define Your State

**File: `agent/graph.py`**
```python
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
import operator

class AgentState(TypedDict):
    query: str                          # Original user question
    messages: List[dict]                # Conversation history
    search_results: List[str]           # Accumulated search results
    total_cost: float                   # Running cost tracker
    iteration: int                      # Loop counter
    route: str                          # "chat" or "research"
    final_answer: str                   # Output to user
    budget_exceeded: bool               # Kill switch flag
    awaiting_approval: bool             # Human-in-the-loop flag
```

### 3.2 Build Node A — The Router

**File: `agent/nodes.py`**
```python
import anthropic
import json

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

    # Calculate this node's cost
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
```

### 3.3 Wire Up the Graph (Router Only)

```python
# agent/graph.py (continued)
from agent.nodes import router_node, route_decision, chat_responder_node

def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("chat_responder", chat_responder_node)

    # Set entry point
    graph.set_entry_point("router")

    # Add conditional edge from router
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "researcher": END,        # placeholder until Phase 4
            "chat_responder": "chat_responder"
        }
    )

    graph.add_edge("chat_responder", END)

    return graph.compile()
```

### 3.4 Test the Router
```python
# Run this to verify routing works before moving on
from agent.graph import build_graph

app = build_graph()

test_queries = [
    "What is FinOps?",                          # should → chat
    "What are the latest AWS pricing changes?",  # should → research
    "How are you today?",                        # should → chat
    "What companies laid off the most in 2025?"  # should → research
]

for query in test_queries:
    result = app.invoke({"query": query, "total_cost": 0.0, "iteration": 0})
    print(f"Query: {query}")
    print(f"Route: {result['route']} | Cost: ${result['total_cost']:.6f}\n")
```

---

## Phase 4: Build the Budget Kill Switch (2–3 hours)

This is the core of the project. Read it carefully.

### 4.1 The Budget Function

**File: `agent/budget.py`**
```python
import os

MAX_BUDGET = float(os.getenv("MAX_BUDGET", "0.05"))

def check_budget(state: dict) -> dict:
    """
    The kill switch. Runs before every research loop.
    Returns updated state with budget_exceeded flag.
    """
    total_cost    = state.get("total_cost", 0.0)
    iteration     = state.get("iteration", 0)
    max_iter      = int(os.getenv("MAX_ITERATIONS", "3"))

    print(f"[Budget] Total cost so far: ${total_cost:.4f} / ${MAX_BUDGET}")

    # Check 1: Budget exceeded
    if total_cost >= MAX_BUDGET:
        print(f"[Budget] 🛑 Threshold reached. Interrupting.")
        return {
            "budget_exceeded": True,
            "awaiting_approval": True,
            "final_answer": (
                f"Budget threshold of ${MAX_BUDGET} reached after {iteration} research loop(s).\n"
                f"Total spent: ${total_cost:.4f}\n\n"
                f"Results so far:\n{_summarize_results(state)}\n\n"
                f"Would you like to spend another ${MAX_BUDGET} to continue? (yes/no)"
            )
        }

    # Check 2: Max iterations reached
    if iteration >= max_iter:
        print(f"[Budget] 🛑 Max iterations ({max_iter}) reached.")
        return {
            "budget_exceeded": True,
            "awaiting_approval": False,
            "final_answer": (
                f"Reached maximum research loops ({max_iter}).\n"
                f"Total spent: ${total_cost:.4f}\n\n"
                f"Here's what I found:\n{_summarize_results(state)}"
            )
        }

    # All clear — continue research
    return {"budget_exceeded": False}


def _summarize_results(state: dict) -> str:
    """Format search results for the interrupt message."""
    results = state.get("search_results", [])
    if not results:
        return "No results collected yet."
    return "\n".join(f"- {r}" for r in results)


def budget_gate(state: dict) -> str:
    """Edge function: routes based on budget check result."""
    if state.get("budget_exceeded"):
        return "end"
    return "researcher"
```

### 4.2 Build Node B — The Researcher

**File: `agent/tools.py`**
```python
from tavily import TavilyClient
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str, max_results: int = 3) -> list[str]:
    """
    Wrapper around Tavily search.
    Returns a clean list of result snippets.
    """
    try:
        results = tavily.search(query=query, max_results=max_results)
        return [r["content"] for r in results.get("results", [])]
    except Exception as e:
        print(f"[Search] Error: {e}")
        return ["Search failed — no results returned."]
```

**Add to `agent/nodes.py`:**
```python
from agent.tools import search_web

# Sonnet pricing (per million tokens)
SONNET_INPUT_COST  = 3.00  / 1_000_000
SONNET_OUTPUT_COST = 15.00 / 1_000_000

def researcher_node(state: dict) -> dict:
    """
    Node B: The expensive node. Only runs when routing says 'research'.
    Uses Sonnet + Tavily search.
    """
    iteration = state.get("iteration", 0) + 1
    print(f"[Researcher] Loop {iteration} | Query: '{state['query']}'")

    # Step 1: Search the web
    search_results = search_web(state["query"])
    all_results    = state.get("search_results", []) + search_results

    # Step 2: Synthesize with Sonnet
    context = "\n\n".join(search_results)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="You are a research assistant. Synthesize the search results into a clear, accurate answer. If you need more information, say so explicitly.",
        messages=[{
            "role": "user",
            "content": f"Question: {state['query']}\n\nSearch Results:\n{context}"
        }]
    )

    input_tokens  = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    node_cost = (input_tokens * SONNET_INPUT_COST) + (output_tokens * SONNET_OUTPUT_COST)

    answer         = response.content[0].text
    needs_more     = "need more information" in answer.lower() or "unclear" in answer.lower()

    print(f"[Researcher] Cost: ${node_cost:.4f} | Needs more: {needs_more}")

    return {
        "search_results": all_results,
        "final_answer":   answer,
        "total_cost":     state["total_cost"] + node_cost,
        "iteration":      iteration,
        "needs_more_research": needs_more
    }


def needs_more_research(state: dict) -> str:
    """Edge: does the researcher want to loop?"""
    if state.get("needs_more_research") and not state.get("budget_exceeded"):
        return "budget_check"   # check budget before looping
    return "end"
```

### 4.3 Wire the Full Graph

```python
# agent/graph.py — full version
from langgraph.graph import StateGraph, END
from agent.nodes import (
    router_node, route_decision,
    chat_responder_node,
    researcher_node, needs_more_research
)
from agent.budget import check_budget, budget_gate

def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("router",         router_node)
    graph.add_node("chat_responder", chat_responder_node)
    graph.add_node("researcher",     researcher_node)
    graph.add_node("budget_check",   check_budget)

    # Entry
    graph.set_entry_point("router")

    # Router → chat or research
    graph.add_conditional_edges("router", route_decision, {
        "researcher":     "budget_check",   # check budget FIRST
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
```

---

## Phase 5: Testing (1–2 hours)

### 5.1 Test Scenarios

```python
# tests/test_agent.py
from agent.graph import build_graph

app = build_graph()

def run(query):
    initial_state = {
        "query": query,
        "messages": [],
        "search_results": [],
        "total_cost": 0.0,
        "iteration": 0,
        "budget_exceeded": False,
        "awaiting_approval": False,
        "final_answer": ""
    }
    result = app.invoke(initial_state)
    print(f"\n{'='*50}")
    print(f"Query:  {query}")
    print(f"Route:  {result.get('route')}")
    print(f"Cost:   ${result['total_cost']:.4f}")
    print(f"Loops:  {result.get('iteration', 0)}")
    print(f"Answer: {result['final_answer'][:200]}...")
    return result

# Test 1: Chat route (should be very cheap)
run("What does FinOps stand for?")

# Test 2: Research route (should trigger search)
run("What are the latest AWS cost optimization announcements in 2025?")

# Test 3: Budget trigger (force with a complex multi-part question)
run("Compare AWS, Azure, and GCP pricing for Lambda-equivalent services, including all recent 2025 changes")
```

### 5.2 Cost Tracking Checklist
- [ ] Chat route costs < $0.001 per query
- [ ] Research route costs $0.02–0.04 per query
- [ ] Budget interrupt fires at $0.05
- [ ] Max iterations stops at 3
- [ ] Cost reported accurately in interrupt message

---

## Phase 6: Deployment to AWS Fargate (2–3 hours)

### Why Fargate, not Lambda?
LangGraph maintains state across multiple loop iterations. Lambda is stateless and times out at 15 minutes. Fargate runs your container as long as needed.

### 6.1 Containerize the Agent

**File: `Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Simple FastAPI wrapper so Fargate has an HTTP endpoint
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

**File: `app.py`**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from agent.graph import build_graph

app    = FastAPI()
agent  = build_graph()

class Query(BaseModel):
    query: str

@app.post("/research")
async def research(q: Query):
    result = agent.invoke({
        "query": q.query,
        "messages": [], "search_results": [],
        "total_cost": 0.0, "iteration": 0,
        "budget_exceeded": False, "awaiting_approval": False,
        "final_answer": ""
    })
    return {
        "answer":    result["final_answer"],
        "cost":      result["total_cost"],
        "route":     result.get("route"),
        "loops":     result.get("iteration", 0),
        "interrupted": result.get("budget_exceeded", False)
    }

@app.get("/health")
def health():
    return {"status": "ok"}
```

### 6.2 Deploy Steps (High Level)
```bash
# 1. Build and push to ECR
aws ecr create-repository --repository-name budget-research-agent
docker build -t budget-research-agent .
docker tag budget-research-agent:latest [ECR_URI]:latest
docker push [ECR_URI]:latest

# 2. Create Fargate task definition (via console or CLI)
# 3. Create ECS cluster + service
# 4. Set environment variables (ANTHROPIC_API_KEY, TAVILY_API_KEY) in task definition
# 5. Test endpoint
curl -X POST https://[your-fargate-url]/research \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest FinOps best practices?"}'
```

---

## Phase 7: Documentation & Portfolio Prep (1 hour)

### README Key Sections
- Architecture diagram (draw.io — same pattern as Cloud Resume Challenge)
- Cost breakdown table
- The `check_budget()` logic explained
- Sample output showing budget interrupt in action
- Deployment instructions

### Substack Article Hook
> "Most AI agent tutorials teach you how to build the agent. Nobody teaches you how to stop it from running up your bill. I built one with a $0.05 kill switch — here's how."

### Portfolio Card Copy
```markdown
#### [Budget-Conscious Research Agent](./budget-research-agent)

**A LangGraph agent that asks permission before spending your money**
Multi-node research agent with a real-time cost tracker and human-in-the-loop 
budget interrupt. Because the same pattern that controls $0.05 controls $50,000.
**Tech:** Python, LangGraph, Claude (Haiku + Sonnet), Tavily, AWS Fargate
🔗 [GitHub](./budget-research-agent)
```

---

## Tagging Strategy

| Tag | Value |
|-----|-------|
| Project | budget-research-agent |
| CostCenter | Project2 |
| Environment | dev |
| Component | agent / api / container |
| ManagedBy | fargate |

---

## Cost Tracker

| Phase | Service | Estimated | Actual |
|-------|---------|-----------|--------|
| Dev | Anthropic API | ~$4.00 | |
| Dev | Tavily | $0.00 | |
| Deploy | Fargate (dev) | ~$0.50/day | |
| Deploy | ECR storage | ~$0.10 | |
| **Total** | | **~$6.00** | |

---

## Changelog

**[DATE]** — Project spec created  
**[DATE]** — Phase 1 complete (environment setup)  
**[DATE]** — Phase 2 complete (LangGraph concepts)  
**[DATE]** — Phase 3 complete (router node working)  
**[DATE]** — Phase 4 complete (budget kill switch + researcher)  
**[DATE]** — Phase 5 complete (testing)  
**[DATE]** — Phase 6 complete (deployed to Fargate)  
**[DATE]** — Phase 7 complete (docs + portfolio)  
**[DATE]** — Substack article published  

---

*Part of the Project Folder portfolio — theprojectfolder.com*  
*Carlandra in the Cloud · Building at the intersection of FinOps and engineering*
